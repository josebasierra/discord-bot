import discord
from speech_generator import SpeechGenerator
from audio_reader import get_audio_from_file, get_audio_from_url

class DiscordBot:

    def __init__(self, bot):
        self.bot = bot
        self.speech_generator = SpeechGenerator()
        self.voice_file_counter = 0  # it's used to know in which file save created voice
    

    async def leave_voice_channel(self, ctx):
        current_voice_client = self.get_current_voice_client(ctx.guild)
        if current_voice_client != None:  
            if (current_voice_client.is_playing()): 
                current_voice_client.stop()
            await current_voice_client.disconnect()


    async def join_voice_channel(self, ctx):
        user_voice = ctx.author.voice
        if(user_voice == None):
            return

        current_voice_client = self.get_current_voice_client(ctx.guild)
        if (current_voice_client != None and current_voice_client.channel != user_voice.channel):
            await current_voice_client.disconnect()

        if (current_voice_client == None): 
            await user_voice.channel.connect() 

        
    async def play_text_audio(self, ctx, text):
        await self.join_voice_channel(ctx)

        # create audio
        audio_file = f'./data/voice{self.voice_file_counter}.mp3'
        self.voice_file_counter = (self.voice_file_counter + 1)%2
        self.speech_generator.create_speech(text, audio_file)
        audio = get_audio_from_file(audio_file)

        self.play_audio(ctx, audio)
    

    async def play_youtube_audio(self, ctx, url):
        await self.join_voice_channel(ctx)

        audio = get_audio_from_url(url)
        self.play_audio(ctx, audio)


    async def send_text(self, ctx, text):
        await ctx.send(text)


    async def notify(self, ctx, textString, audioString=None):
        await self.send_text(ctx, textString)
        if (audioString != None): 
            await self.play_text_audio(ctx, audioString)


    def play_audio(self, ctx, audio):
        voice = self.get_current_voice_client(ctx.guild)
        if not voice:
            return

        if (voice.is_playing()): 
            voice.stop()

        voice.play(audio)


    def get_current_voice_client(self, guild):
        for voice_client in self.bot.voice_clients:
            if (voice_client.guild == guild):
                return voice_client
        
        return None




        


