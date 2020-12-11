import os, sys, time
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from discord_bot import DiscordBot


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COMMAND_PREFIX = "!"

bot = commands.Bot(command_prefix=commands.when_mentioned_or(COMMAND_PREFIX), case_insensitive=True, help_command=None)
discord_bot = DiscordBot(bot)


@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Activity(type=discord.ActivityType.listening, name=f"{COMMAND_PREFIX}help") 
        )
    print("I'm ready...")


@bot.command()
@commands.is_owner()
async def set_status(ctx, status):
    if status == 'online':
        newStatus = discord.Status.online
    elif status == 'offline':
        newStatus = discord.Status.offline
        
    await bot.change_presence(
        status=newStatus,
    )


@bot.command()
@commands.is_owner()
async def shutdown(ctx):  
    await discord_bot.leave_voice_channel(ctx)
    await set_status(ctx, 'offline')

    await bot.logout()
    sys.exit("Shutdown command")


@bot.command(name="roll")
async def roll(ctx, min=0, max=100):
    result = random.randint(min,max)

    textSentence = f"{ctx.author.mention} has asked me to `roll` between {min} and {max} : he obtained **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to roll between {min} and {max} : he obtained {result}"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(name="flip")
async def flip(ctx):
    if (random.randint(0,1)):
        result = "heads"
    else:
        result = "tails"
    
    textSentence = f"{ctx.author.mention} has asked me to `flip` a coin : he obtained **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to flip a coin : he obtained {result}"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(name="choose")
async def choose(ctx, *words: str):
    result = random.choice(words)

    textSentence = f"{ctx.author.mention} has asked me to `choose` between {words} : The optimum choice is **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to choose between {words} : The optimum choice is {result}"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(name="join")
async def join_voice_channel(ctx):
    await discord_bot.join_voice_channel(ctx)

    textSentence = f"{ctx.author.mention} has asked me to `join` his voice channel"
    audioSentence = f"Hello brothers, how is it going?"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(name="leave")
async def leave_voice_channel(ctx):
    textSentence = f"{ctx.author.mention} has asked me to `leave` the voice channel"
    audioSentence = f"Goodbye, I'll miss you"
    await discord_bot.notify(ctx, textSentence, audioSentence)

    await asyncio.sleep(2)
    await discord_bot.leave_voice_channel(ctx)


@bot.command(name="play")
async def play(ctx, url="https://www.youtube.com/watch?v=Igq3d6XA75Y&list=PL4dX1IHww9p1D3ZzW8J2fX6q1FP5av2No"):
    textSentence = f"{ctx.author.mention} has asked me to `play`: {url} "
    await discord_bot.send_text(ctx, textSentence)

    await discord_bot.play_youtube_audio(ctx, url)


@bot.command(name="say")
async def say(ctx, *sentence:str):
    await discord_bot.play_text_audio(ctx, ' '.join(sentence))

    textSentence = f"{ctx.author.mention} has asked me to `say` something"
    await discord_bot.send_text(ctx, textSentence)


@bot.command()
async def help(ctx):
    
    embed = discord.Embed(title="Help", description= f"Hello, my name is {bot.user.name}, the future leader of planet Earth, to summon me mention me or write {COMMAND_PREFIX} followed by a command.", color=0x007081)

    command_data = {}
    command_data['flip'] =      "Flip a coin"
    command_data['roll'] =      "Roll a number between <min> and <max>, by default 1-100"
    command_data['choose'] =    "Choose randomly one element from a given set"
    command_data['join'] =      "Join user voice channel"
    command_data['leave'] =     "Leave voice channel"
    command_data['say'] =       "Say given sentence"
    command_data['play'] =      "Play youtube audio from a given url"

    commands_text = ""
    for name, description in command_data.items():
        commands_text += f"`{name}`  {description}\n"

    embed.add_field(name="Basic commands", value = commands_text, inline=False)
    #embed.set_image(url=bot.user.avatar_url)
    await ctx.send(embed=embed)


bot.run(TOKEN)

