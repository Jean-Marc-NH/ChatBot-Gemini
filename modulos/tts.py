import pyttsx3
from config import TTS_CONFIG

class TextSpeaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        if "rate" in TTS_CONFIG:
            self.engine.setProperty('rate', TTS_CONFIG['rate'])
        if "volume" in TTS_CONFIG:
            self.engine.setProperty('volume', TTS_CONFIG['volume'])

    def speak(self, text: str) -> None:
        self.engine.say(text)
        self.engine.runAndWait()
