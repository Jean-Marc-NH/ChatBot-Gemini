import speech_recognition as sr
from config import STT_CONFIG

class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        if "energy_threshold" in STT_CONFIG:
            self.recognizer.energy_threshold = STT_CONFIG["energy_threshold"]
        if "pause_threshold" in STT_CONFIG:
            self.recognizer.pause_threshold = STT_CONFIG["pause_threshold"]
        self.language = STT_CONFIG.get("language", "es-ES")

    def listen(self) -> str:
        with sr.Microphone() as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            text = self.recognizer.recognize_google(audio, language=self.language)
            print(f"Usuario dijo: {text}")
            return text
        except sr.UnknownValueError:
            print("No entendí lo que dijiste.")
            return ""
        except sr.RequestError as e:
            print(f"Error al conectar con el servicio STT: {e}")
            return ""