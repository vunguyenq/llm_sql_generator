import logging
import re
from typing import Type, Union
from pydantic import BaseModel
from pathlib import Path
from src.context.structured_output import SQLGeneration
from src.executors import query_builder
from openai import AzureOpenAI, OpenAI

import src.config as config

OPENAI_API_KEY = config.OPENAI_API_KEY


def extract_sql_from_response(response: str) -> str:
    return response.strip().replace('```sql', '').replace('```', '')

def query_open_ai(prompt: str, model: str = 'gpt-4o') -> str:
    """Sends a prompt to GPT-4 with structured roles."""
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": query_builder.create_system_context()},
                {"role": "user", "content": query_builder.format_user_prompt(prompt)}
            ],
            max_tokens=3000
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return ""

def query_azure_open_ai(messages: str, response_format: Type[BaseModel] = None, log: bool = False) -> Union[str, Type[BaseModel]]:
    """Sends a prompt to GPT-4.
    If response_format is not provided, returns result in structured output.
    Otherwise, returns json content of output message."""
    if log:
        logging.info(f"Query prompt: {messages}")  
        
    if not response_format:
        response_format = SQLGeneration

    try:
        client = AzureOpenAI(azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
                             api_key=config.AZURE_OPENAI_API_KEY,
                             api_version=config.AZURE_OPENAI_API_VERSION
                             )
        response = client.beta.chat.completions.parse(
            model=config.AZURE_OPENAI_DEPLOYMENT,
            messages=messages,
            response_format=response_format,
            max_tokens=3000
        )

    except Exception as e:
        print(f"Error: {e}")
        logging.error(f"Query failed: {e}")
        return ""

    if log:
        logging.info(f"Query response: {response.choices[0].message.content}")
        logging.info(f"Prompt tokens: {response.usage.prompt_tokens}. Completion tokens: {response.usage.completion_tokens}. Total tokens: {response.usage.total_tokens}")
    
    if response_format:
        return response.choices[0].message.parsed
    return response.choices[0].message.content
