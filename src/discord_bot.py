import discord
from voice_engine import VoiceEngine
from audio_reader import get_audio_from_file, get_audio_from_url

class DiscordBot:

    def __init__(self, bot):
        self.bot = bot
        self.voice_engine = VoiceEngine()
    

    async def leave_voice_channel(self, ctx):
        current_voice_client = self.get_current_voice_client(ctx.guild)
        if current_voice_client != None:
            await current_voice_client.disconnect()


    #TODO: clean this shit
    async def join_voice_channel(self, ctx):

        user_voice = ctx.author.voice
        if(user_voice == None):
            return

        current_voice_client = self.get_current_voice_client(ctx.guild)
        if (current_voice_client != None and current_voice_client.channel != user_voice.channel):
            await current_voice_client.disconnect()
            await user_voice.channel.connect()

        if (current_voice_client == None): 
            await user_voice.channel.connect() 

        
    async def play_text_audio(self, ctx, text):
        await self.join_voice_channel(ctx)

        # create audio
        default_path = './data/voice.mp3'
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
        if (audioString != None): 
            await self.play_text_audio(ctx, audioString)


    def play_audio(self, ctx, audio):
        voice = discord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice:
            voice.stop()
            voice.play(audio)


    def get_current_voice_client(self, guild):
        for voice_client in self.bot.voice_clients:
            if (voice_client.guild == guild):
                return voice_client
        
        return None




        


