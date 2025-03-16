import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))  # allow importing from /src

from src import config
from src.utils.logging_utils import setup_logging
from openai import AzureOpenAI
from pydantic import BaseModel, Field

setup_logging("logs")

client = AzureOpenAI(azure_endpoint=config.AZURE_OPENAI_ENDPOINT,
                             api_key=config.AZURE_OPENAI_API_KEY,
                             api_version=config.AZURE_OPENAI_API_VERSION
                             )
class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str
    # famous_quote: str = Field(..., description="A famous quote that is not related to math.")

completion = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages=[
        {"role": "system", "content": "You are a helpful math tutor. Guide the user through the solution step by step."},
        {"role": "user", "content": "How can I solve 8x + 7 = -23?"}
    ],
    response_format=MathReasoning,
)

math_reasoning = completion.choices[0].message.parsed

print("Steps:", math_reasoning.steps)
print("Final Answer:", math_reasoning.final_answer)
print(f"Prompt tokens: {completion.usage.prompt_tokens}. Completion tokens: {completion.usage.completion_tokens}. Total tokens: {completion.usage.total_tokens}")
# print("Quote:", math_reasoning.famous_quote)
