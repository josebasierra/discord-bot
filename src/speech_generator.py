import pyttsx3
from audio_reader import get_audio_from_file, get_audio_from_url

class SpeechGenerator:

    def __init__(self, speed = 170, volume=1, voiceNumber=1):
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', speed)
        self.engine.setProperty('volume', volume)
        self.set_voice(1) # set David voice default (it depends on windows installed voices)
    

    def play(self, text):
        self.engine.say(text)
        self.engine.runAndWait()


    def create_speech(self, text, filePath):
        self.engine.save_to_file(text, filePath)
        self.engine.runAndWait()


    def get_available_voices(self):
        return [voice.id for voice in self.engine.getProperty('voices')]
    

    def set_voice(self, voiceNumber):
        voices = self.get_available_voices()
        if voiceNumber < len(voices):
            self.engine.setProperty('voice', voices[voiceNumber])
        else:
            print("Incorrect voice number")




