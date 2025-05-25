from config import SESSION_MAX_TURNS

def build_prompt(system_prompt: str, history: list, user_input: str) -> str:
    max_entries = SESSION_MAX_TURNS * 2
    recent = history[-max_entries:] if len(history) > max_entries else history

    prompt_parts = []
    if system_prompt:
        prompt_parts.append(f"<SYSTEM> {system_prompt}")
    for turn in recent:
        speaker = turn.get('speaker', 'Usuario')
        text = turn.get('text', '')
        prompt_parts.append(f"{speaker}: {text}")
    prompt_parts.append(f"Usuario: {user_input}")
    prompt_parts.append("IA:")  

    return "\n".join(prompt_parts)
