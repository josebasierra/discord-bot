import os, sys, time
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from discord_bot import DiscordBot


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
discord_bot = DiscordBot(bot)

@bot.event
async def on_ready():
    await bot.change_presence(
        status=discord.Status.online
        )
    print("Hello!")


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
    await ctx.message.delete()

    await discord_bot.leave_voice_channel(ctx)
    await set_status(ctx, 'offline')

    await bot.logout()
    sys.exit("Shutdown command")



@bot.command(help= 'Roll random number between <min> and <max>')
async def roll(ctx, min=0, max=100):
    result = random.randint(min,max)

    textSentence = f"{ctx.author.mention} has asked me to `roll` : he obtained **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to roll : he obtained {result}"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(help= 'Flip coin, get heads or tails')
async def flip(ctx):
    if (random.randint(0,1)):
        result = "heads"
    else:
        result = "tails"
    
    textSentence = f"{ctx.author.mention} has asked me to `flip` a coin : **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to flip a coin: {result}"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(name="choose", description='Random choice between words')
async def choose(ctx, *words: str):
    result = random.choice(words)

    textSentence = f"{ctx.author.mention} has asked me to `choose` between {words} : The optimum choice is **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to choose between {words} : The optimum choice is {result}"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(name="join", description="Join current voice channel")
async def join_voice_channel(ctx):
    await discord_bot.join_voice_channel(ctx)

    textSentence = f"{ctx.author.mention} has asked me to `join` his voice channel"
    audioSentence = f"Hello brothers, how is it going?"
    await discord_bot.notify(ctx, textSentence, audioSentence)


@bot.command(name="leave", description="Leave voice channel if possible")
async def leave_voice_channel(ctx):
    textSentence = f"{ctx.author.mention} has asked me to `leave` the voice channel"
    audioSentence = f"Goodbye, I'll miss you"
    await discord_bot.notify(ctx, textSentence, audioSentence)

    time.sleep(2)
    await discord_bot.leave_voice_channel(ctx)


@bot.command(name="play", description="play <url> Plays youtube video")
async def play(ctx, url="https://www.youtube.com/watch?v=Igq3d6XA75Y&list=PL4dX1IHww9p1D3ZzW8J2fX6q1FP5av2No"):
    textSentence = f"{ctx.author.mention} has asked me to `play`: {url} "
    await discord_bot.send_text(ctx, textSentence)

    await discord_bot.play_youtube_audio(ctx, url)


@bot.command(name="say", description="Narrates the given text")
async def say(ctx, *sentence:str):
    await discord_bot.play_text_audio(ctx, ' '.join(sentence))

    textSentence = f"{ctx.author.mention} has asked me to `say` something"
    await discord_bot.send_text(ctx, textSentence)


def get_sentence(author, action, result):
    print(author.mention)
    message = f"{author.mention} has asked me to `{action}` : **{result}**"
    return(message)


bot.run(TOKEN)






# @bot.event
# async def on_message(message):
#     if bot.user.mentioned_in(message):
#         print(message.content)
#         await message.channel.send("...")


# @bot.command()
# async def help(context):
#     await context.send("Custom help command")


#embed example
#embed=discord.Embed(title="flip!", description=result, color=0xffffff)
#await ctx.send(embed=embed)