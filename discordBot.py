import discord
from voiceEngine import VoiceEngine
from audioReader import get_audio_from_file, get_audio_from_url

class DiscordBot:

    def __init__(self, bot):
        self.bot = bot
        self.voice_engine = VoiceEngine()
    

    async def leave_voice_channel(self, ctx):
        for voice_client in self.bot.voice_clients:
            await voice_client.disconnect()

    #TODO: do not leave channel if connected in it
    async def join_voice_channel(self, ctx):
        await self.leave_voice_channel(ctx)
        voice = ctx.author.voice
        if voice:
            await voice.channel.connect()


    async def play_text_audio(self, ctx, text):
        await self.join_voice_channel(ctx)

        # create audio
        default_path = './voice.mp3'
        self.voice_engine.create_voice_file(text, default_path)
        audio = get_audio_from_file(default_path)

        self.play_audio(ctx, audio)
    

    async def play_youtube_audio(self, ctx, url="https://www.youtube.com/watch?v=Igq3d6XA75Y&list=PL4dX1IHww9p1D3ZzW8J2fX6q1FP5av2No"):
        await self.join_voice_channel(ctx)

        audio = get_audio_from_url(url)
        self.play_audio(ctx, audio)


    async def send_text(self, ctx, text):
        await ctx.send(text)


    async def notify(self, ctx, textString, audioString):
        await self.send_text(ctx, textString)
        await self.play_text_audio(ctx, audioString)


    def play_audio(self, ctx, audio):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and not voice.is_playing():
            voice.play(audio)



        


