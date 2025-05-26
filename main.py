from modulos import SpeechRecognizer, TextSpeaker, GeminiChat, MemoryManager, build_prompt, SpotifyController
from config import EXIT_PHRASES
from dotenv import load_dotenv
load_dotenv()

def main():
    stt = SpeechRecognizer()
    tts = TextSpeaker()
    memoria = MemoryManager("Jean-Marc")
    gemini = GeminiChat(memoria)
    spotify = SpotifyController(usuario_id="Jean-Marc")

    tts.speak("Hola. ¿En qué puedo ayudarte hoy?")

    while True:
        user_input = stt.listen()
        if not user_input:
            continue

        if user_input.lower() in EXIT_PHRASES:
            tts.speak("Hasta luego!")
            break

        if gemini.clasificar_comando(user_input) == "spotify":
            intencion = gemini.extraer_intencion_musical(user_input)
            tipo = intencion.get("tipo")
            valor = intencion.get("valor")
            print(tipo + " " + valor)

            if tipo == "ninguno":
                respuesta = "No entendí qué música querés escuchar."
            else:
                respuesta = spotify.reproducir(tipo, valor)

        else:
            system_prompt = memoria.build_system_prompt()
            prompt = build_prompt(system_prompt, gemini.history, user_input)
            respuesta = gemini.send_message(prompt)

        tts.speak(respuesta)

if __name__ == "__main__":
    main()
