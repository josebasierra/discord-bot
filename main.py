import os
import random

import discord
from discord.ext import commands
from dotenv import load_dotenv

from discordBot import DiscordBot


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))
discordBot = DiscordBot(bot)

@bot.event
async def on_ready():
    print("Hello!")


@bot.command()
async def test(ctx):
    await ctx.send(ctx.guild.default_role)


@bot.command(help= 'Roll random number between <min> and <max>')
async def roll(ctx, min=0, max=100):
    result = random.randint(min,max)

    textSentence = f"{ctx.author.mention} has asked me to `roll` : he obtained **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to roll : he obtained {result}"
    await discordBot.notify(ctx, textSentence, audioSentence)


@bot.command(help= 'Flip coin, get heads or tails')
async def flip(ctx):
    if (random.randint(0,1)):
        result = "heads"
    else:
        result = "tails"
    
    textSentence = f"{ctx.author.mention} has asked me to `flip` a coin : **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to flip a coin: {result}"
    await discordBot.notify(ctx, textSentence, audioSentence)


@bot.command(name="choose", description='Random choice between words')
async def choose(ctx, *words: str):
    result = random.choice(words)

    textSentence = f"{ctx.author.mention} has asked me to `choose` between {words} : The optimum choice is **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to choose between {words} : The optimum choice is {result}"
    await discordBot.notify(ctx, textSentence, audioSentence)


@bot.command(name="join", description="Join current voice channel")
async def join_voice_channel(ctx):
    await discordBot.join_voice_channel(ctx)

    textSentence = f"{ctx.author.mention} has asked me to `join` his voice channel"
    audioSentence = f"Hello brothers, how is it going?"
    await discordBot.notify(ctx, textSentence, audioSentence)

#TODO: fix
@bot.command(name="leave", description="Leave voice channel if possible")
async def leave_voice_channel(ctx):
    textSentence = f"{ctx.author.mention} has asked me to `leave` the voice channel"
    audioSentence = f"Goodbye, I'll miss ya"
    await discordBot.notify(ctx, textSentence, audioSentence)

    await discordBot.leave_voice_channel(ctx)


@bot.command(name="play", description="play <url> Plays youtube video")
async def play(ctx, url="https://www.youtube.com/watch?v=Igq3d6XA75Y&list=PL4dX1IHww9p1D3ZzW8J2fX6q1FP5av2No"):
    textSentence = f"{ctx.author.mention} has asked me to `play`: {url} "
    audioSentence = f"Reproducing video in 3,2,1"
    await discordBot.notify(ctx, textSentence, audioSentence)

    await discordBot.play_youtube_audio(ctx, url)


@bot.command(name="say", description="Narrates the given text")
async def say(ctx, *sentence:str):
    await discordBot.play_text_audio(ctx, ' '.join(sentence))

    textSentence = f"{ctx.author.mention} has asked me to `say` something"
    await discordBot.send_text(ctx, textSentence)


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