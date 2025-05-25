from modulos import SpeechRecognizer, TextSpeaker, GeminiChat, MemoryManager, build_prompt
from config import EXIT_PHRASES

from dotenv import load_dotenv
load_dotenv()

def main():
    stt = SpeechRecognizer()
    tts = TextSpeaker()
    memoria = MemoryManager("Jean-Marc")
    gemini = GeminiChat(memoria)

    tts.speak("Hola. ¿En qué puedo ayudarte hoy?")

    while True:
        user_input = stt.listen()
        if not user_input:
            continue

        if user_input.lower() in EXIT_PHRASES:
            tts.speak("Hasta luego!")
            break

        system_prompt = memoria.build_system_prompt()
        prompt = build_prompt(system_prompt, gemini.history, user_input)

        respuesta = gemini.send_message(prompt)

        tts.speak(respuesta)


if __name__ == "__main__":
    main()