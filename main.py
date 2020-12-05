import os
import random
import time

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv

from audioReader import *
from voiceEngine import VoiceEngine
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
    await ctx.send(get_sentence(ctx.author, "roll", result ))


@bot.command(help= 'Flip coin, get heads or tails')
async def flip(ctx):
    print(ctx.author)
    if (random.randint(0,1)):
        result = "heads"
    else:
        result = "tails"

    textSentence = f"{ctx.author.mention} has asked me to `flip` : he obtained **{result}**"
    audioSentence = f"{ctx.author.name} has asked me to flip : he obtained {result}"
    await ctx.send(textSentence)
    await discordBot.playTextAudio(ctx, audioSentence)




@bot.command(name="choose", description='Random choice between words')
async def choose(ctx, *words: str):
    await ctx.send(get_sentence(ctx.author, "choose", random.choice(words)))


@bot.command(name="join", description="Join current voice channel")
async def join_voice_channel(ctx):
    await discordBot.join_voice_channel(ctx)


@bot.command(name="leave", description="Leave voice channel if possible")
async def leave_voice_channel(ctx):
    await discordBot.leave_voice_channel(ctx)


@bot.command(name="play", description="play <url> Plays youtube video")
async def play(ctx, url="https://www.youtube.com/watch?v=Igq3d6XA75Y&list=PL4dX1IHww9p1D3ZzW8J2fX6q1FP5av2No"):
    await discordBot.playYoutubeAudio(ctx, url)


@bot.command(name="say", description="Narrates the given text")
async def say(ctx, *sentence:str):
    await discordBot.playTextAudio(ctx, ' '.join(sentence))

    textSentence = f"{ctx.author.mention} has asked me to `say` something"
    await ctx.send(textSentence)




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