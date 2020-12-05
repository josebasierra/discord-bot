import os
import random
import time

import discord
from discord.ext.commands import Bot
from discord.ext import commands
from dotenv import load_dotenv

from helpers import get_audio


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

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

    await ctx.send(get_sentence(ctx.author, "flip", result))


@bot.command(description='Random choice between words')
async def choose(ctx, *words: str):
    await ctx.send(get_sentence(ctx.author, "choose", random.choice(words)))


@bot.command(name="join", description="Join current voice channel")
async def join_voice_channel(ctx):
    await leave_voice_channel(ctx)
    voice = ctx.author.voice
    if voice:
        await voice.channel.connect()


@bot.command(name="leave", description="Leave voice channel if possible")
async def leave_voice_channel(ctx):
    for voice_client in bot.voice_clients:
        await voice_client.disconnect()


@bot.command(description="play <url> Plays youtube video")
async def play(ctx, url="https://www.youtube.com/watch?v=Igq3d6XA75Y&list=PL4dX1IHww9p1D3ZzW8J2fX6q1FP5av2No"):

    voice = discord.utils.get(bot.voice_clients, guild=ctx.guild)
    if not voice.is_playing():
        voice.play(get_audio(url))
        voice.is_playing()
    else:
        await ctx.send("Already playing song")
        return


def get_sentence(author, action, result):
    print(author.mention)
    message = f"{author.mention} has asked for `{action}` : **{result}**"
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