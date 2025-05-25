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