import re
from pathlib import Path
from src.context.few_shot_examples import create_fewshots_assistant_answers

def create_system_context() -> str:
    current_dir = Path(__file__).parent.parent
    system_context = (current_dir / "context" / 'system_context.txt').read_text()
    erd = (current_dir / "context" / 'database_erd.mermaid').read_text()
    system_context = system_context.replace('{{DATABASE_SCHEMA}}', erd)
    return system_context

def parse_type_hint(prompt: str) -> str:
    """Detects and converts hints like '[type: field]' to explicit sentences."""
    pattern = r"\[(\w+):\s*(\w+)\]$"
    match = re.search(pattern, prompt)

    if match:
        data_type, field_name = match.groups()
        explicit_sentence = f"Return a {field_name} as {data_type}"
        prompt = re.sub(pattern, explicit_sentence, prompt)
    return prompt

def format_user_prompt(prompt: str) -> str:
    return f"{parse_type_hint(prompt)}. Answer with only the SQL statement."

def create_query_message(prompt: str) -> list[dict]:
    return [{"role": "system", "content": create_system_context()},
            *create_fewshots_assistant_answers(),
            {"role": "user", "content": prompt}
