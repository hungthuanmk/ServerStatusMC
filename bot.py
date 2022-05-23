from datetime import datetime
from http import server
import os
import random
from dotenv import load_dotenv
import discord
from discord.ext import commands

from server_status import get_server_status

load_dotenv()
TOKEN = os.getenv('TOKEN')
CLIENT_ID = os.getenv('CLIENT_ID')
GUILD_ID = os.getenv('GUILD_ID')

DEFAULT_CHANNEL = os.getenv('DISCORD_DEFAULT_CHANNEL')
URL_DEFAULT= os.getenv('URL_DEFAULT')
PORT_DEFAULT= os.getenv('PORT_DEFAULT')

bot = commands.Bot(command_prefix='^')

default_message = ''
auto = True

# Display the date today
def get_today(timestamp):
    now = datetime.fromtimestamp(int(timestamp))
    return now.strftime("%d/%m/%Y, %H:%M:%S")

# Display the online status embed
def get_embed():
    description = "Server Status for " + URL_DEFAULT + ":" + PORT_DEFAULT
    embed = discord.Embed(color=discord.Color.purple(), description=description)

    author_name = "Creeper Status: Minecraft Server Status"
    embed.set_author(name=author_name,
                        icon_url='https://art.pixilart.com/b2c52c8e418893c.png')
    embed.set_thumbnail(
        url='https://www.clipartkey.com/mpngs/m/214-2147759_zombie-clipart-minecraft-minecraft-steve-holding-diamond.png')
    server_status = get_server_status(URL_DEFAULT, PORT_DEFAULT)
    
    if server_status and server_status['online']:
        # Server is online
        embed.title = ":green_circle: Server is Online"
        
        embed.add_field(name="MOTD Update", value=server_status['motd'].split(" on ")[1], inline="true")
        embed.add_field(name="Version", value=server_status['server']['name'], inline="true")
        embed.add_field(name="Max Player", value=server_status['players']['max'], inline="true")
        
        if server_status['players']['now'] > 0:
            embed.add_field(name="Players", value="\n".join(player["name"] for player in server_status['players']['sample']), inline="true")
        else:
            embed.add_field(name="Players", value="hem có ai", inline="true")
        embed.add_field(name="Now playing", value=server_status['players']['now'], inline="true")
        
        embed.add_field(name="\u200B", value='\u200B')
        
        embed.set_footer(text="Vào chơi đi check cái éo gì 😏 updated " + get_today(server_status['last_updated']))
        return embed
    
    # Server is offline
    embed.title = ":red_circle: Server is Offline"
    embed.add_field(name="Waiting for the server to open...", value='\u200B')
    embed.set_footer(text="Server chưa mở ngồi đợi đi 😏 updated " + get_today(server_status['last_updated']))
    return embed

# Display icon


def get_icon():
    icons = ['😺', '😸', '😹', '😻', '😼', '😽', '🙀', '😿', '😾']
    return random.choice(icons) + ' '

# Check wheather the bot is connected or not
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# say something interact with user


@bot.event
async def on_message(message):
    global default_message
    # the bot is just ignore itself
    if message.author == bot.user:
        return

    # setup and clear can be use everywhere in server
    if message.channel.name != DEFAULT_CHANNEL:
        if str(message.content) == '^setup':
            # do nothing
            pass
        else:
            return
    # i just want to say hello you
    if message.content.lower().startswith('hello') or message.content.startswith('hi'):

        msg = get_icon() + 'Hello, {0.author.mention}!'.format(message)
        await message.channel.send(msg)

    # think that i'm Tran Duc Bo
    if message.content.lower().startswith('mèo méo'):
        msg = get_icon() + 'con mèo ngu ngốc ngọt ngào đáng yêu cute phô mai que xin chào cả nhà'
        await message.channel.send(msg)

    # what does the cat say ?????
    if message.content.lower().startswith('meow') or message.content.lower().startswith('Meow'):
        msg = get_icon() + 'gàoooooooo~'
        await message.channel.send(msg)

    # this is the main message :'> but has not in dev yet
    if message.content.lower().startswith('auto'):
        embed = get_embed()
        await default_message.edit(embed=embed)

    if message.content.lower().startswith('update'):
        embed = get_embed()
        await default_message.edit(embed=embed)

    if message.content.lower().startswith('server'):
        embed = get_embed()
        await message.channel.send(embed=embed)


    await bot.process_commands(message)
    await message.delete()




@bot.command(name='meow', help='Hmm, I just wanna say hello')
async def say_hello(ctx):
    response = get_icon() + "nyan~ nyan~"
    await ctx.send(response)


@bot.command(name='roll', help='Simulates rolling dice.')
async def roll(ctx, number_of_dice=1, number_of_sides=6):
    dice = [
        str(random.choice(range(1, number_of_sides + 1)))
        for _ in range(number_of_dice)
    ]
    message = get_icon() + 'Tao cho mày nè: ' + ', '.join(dice)
    await ctx.send(message)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        msg = 'Mày hỏng có quyền kêu tao làm như vậy. ' + get_icon()
        await ctx.send(msg)


@bot.command(name='clear', help='Purge message with a number')
async def clear(ctx, amount=100):
    if amount > 500:
        amount = 500
    await ctx.channel.purge(limit=amount)


@bot.command(name='setup', help='Create a workspace for bot to interact')
async def create_channel(ctx, channel_name=DEFAULT_CHANNEL):
    global default_message
    guild = ctx.guild
    existing_channel = discord.utils.get(guild.channels, name=channel_name)
    if not existing_channel:
        print(f'Creating a new channel: {channel_name}')
        await guild.create_text_channel(channel_name)
        
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        embed = await bot.get_channel(existing_channel.id).send(embed=get_embed())
        
        default_message = embed

        message = '😼 Qua ' + '<#' + \
            str(existing_channel.id) + '> chơi với tao!'
        await ctx.send(message)
    else:
        message = '😾 Tao tạo rồi, qua <#' + \
            str(existing_channel.id) + '> kiếm tao nè!'
        await ctx.send(message)

bot.run(TOKEN)
