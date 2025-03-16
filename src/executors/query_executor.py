import logging
import re
from pathlib import Path

from openai import AzureOpenAI, OpenAI

import src.config as config

OPENAI_API_KEY = config.OPENAI_API_KEY

def create_system_context() -> str:
    current_dir = Path(__file__).parent
    system_context = (current_dir / 'system_context.txt').read_text()
    erd = (current_dir / 'database_erd.mermaid').read_text()
    return f"{system_context}\n```mermaid{erd}```"

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

def extract_sql_from_response(response: str) -> str:
    return response.strip().replace('```sql', '').replace('```', '')

def query_open_ai(prompt: str, model: str = 'gpt-4o') -> str:
    """Sends a prompt to GPT-4 with structured roles."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": create_system_context()},
                {"role": "user", "content": format_user_prompt(prompt)}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return ""

def query_azure_open_ai(messages: str, log: bool = False) -> str:
    """Sends a prompt to GPT-4 with structured roles."""
    if log:
        logging.info(f"Query prompt: {messages}")  

    try:
        client = AzureOpenAI(azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
                             api_key=config.AZURE_OPENAI_API_KEY,
                             api_version=config.AZURE_OPENAI_API_VERSION
                             )
        response = client.chat.completions.create(
            model=config.AZURE_OPENAI_DEPLOYMENT,
            messages=messages
        )

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Query failed: {e}")
        return ""

    if log:
        logging.info(f"Query response: {response.choices[0].message.content}")
        logging.info(f"Prompt tokens: {response.usage.prompt_tokens}. Completion tokens: {response.usage.completion_tokens}. Total tokens: {response.usage.total_tokens}")       
    return response.choices[0].message.content
