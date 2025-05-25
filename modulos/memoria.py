import json
from pathlib import Path
from config import USERS_DIR, MEMORY_FILE

class MemoryManager:
    def __init__(self, user_id: str):
        self.user_dir = USERS_DIR / user_id
        self.pref_file = self.user_dir / "preferencias.json"
        self.global_mem_file = MEMORY_FILE
        self.preferences = {}
        self.global_memory = {}
        self._load_files()

    def _load_files(self):
        if self.pref_file.exists():
            with open(self.pref_file, 'r', encoding='utf-8') as f:
                self.preferences = json.load(f)
        else:
            self.user_dir.mkdir(parents=True, exist_ok=True)
            self.preferences = {}
        if self.global_mem_file.exists():
            with open(self.global_mem_file, 'r', encoding='utf-8') as f:
                self.global_memory = json.load(f)
        else:
            self.global_memory = {}

    def build_system_prompt(self) -> str:
        parts = []
        if self.preferences:
            pref_text = f"Usuario: {self.preferences.get('nombre', '')}. " + \
                        f"gustos: {', '.join(self.preferences.get('Gustos', []))}. " + \
                        f"informacion-relevante: {self.preferences.get('informacion-relevante', 'tono: informal')}. "
            parts.append(pref_text)
        user_mem = self.global_memory.get(self.preferences.get('nombre', ''), {})
        if user_mem:
            mem_items = []
            for k, v in user_mem.items():
                mem_items.append(f"{k}: {v}")
            parts.append("Memoria previa: " + ", ".join(mem_items))
        if parts:
            return "".join(parts) + "\n"
        return ""

    def update_memory(self, fact_key: str, fact_value):
        user_name = self.preferences.get('nombre', '')
        if not user_name:
            return
        if user_name not in self.global_memory:
            self.global_memory[user_name] = {}
        self.global_memory[user_name][fact_key] = fact_value
        self.global_mem_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.global_mem_file, 'w', encoding='utf-8') as f:
            json.dump(self.global_memory, f, ensure_ascii=False, indent=2)