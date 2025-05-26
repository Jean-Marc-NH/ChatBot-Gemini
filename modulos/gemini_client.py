import google.generativeai as genai
from config import GEMINI_API_KEY, GEMINI_MODEL, SESSION_MAX_TURNS

class GeminiChat:
    def __init__(self, memory_manager):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)
        self.history = [] 
        self.mem_mgr = memory_manager

    def send_message(self, user_input):
        prompt = self.mem_mgr.build_system_prompt() + self.build_history() + user_input
        resp = self.model.generate_content(prompt)
        self._update_history("IA", resp.text)
        return resp.text

    def _update_history(self, speaker, text):
        self.history.append({"speaker": speaker, "text": text})
        if len(self.history) > SESSION_MAX_TURNS * 2:
            self.history = self.history[-SESSION_MAX_TURNS * 2 :]
            
    def build_history(self):
        historial = ""
        for turno in self.history[-SESSION_MAX_TURNS:]:
            role = turno.get("role", "Usuario")
            content = turno.get("content", "")
            historial += f"\n{role}: {content}"
        return historial

    def clasificar_comando(self, texto_usuario):
        prompt = (
            "Clasifica el siguiente comando. "
            "Responde solo con 'spotify' si es para controlar música en Spotify, "
            "o 'otro' si no tiene relación:\n"
            f"Comando: {texto_usuario}"
        )
        decision = self.model.generate_content(prompt).text.strip().lower()

        return decision
    
    def extraer_intencion_musical(self, mensaje: str) -> dict:
        prompt = (
            "Extrae la intención musical del siguiente mensaje del usuario. "
            "Devuelve un JSON con dos claves: 'tipo' (puede ser 'cancion', 'artista', 'playlist' o 'genero') "
            "y 'valor' (el contenido correspondiente). "
            "Si no se puede identificar, devuelve {'tipo': 'ninguno', 'valor': ''}.\n\n"
            f"Mensaje: {mensaje}\n"
            "Respuesta JSON:"
        )
        respuesta = self.model.generate_content(prompt).text.strip()

        import json
        import re
        try:
            # Buscar el primer bloque que parezca un JSON
            coincidencias = re.findall(r"\{.*?\}", respuesta, re.DOTALL)
            for bloque in coincidencias:
                try:
                    print(bloque)
                    return json.loads(bloque)
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            pass
        return {"tipo": "ninguno", "valor": ""}