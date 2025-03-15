from openai import AzureOpenAI
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import os

load_dotenv()
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT")


client = AzureOpenAI(azure_endpoint=AZURE_OPENAI_ENDPOINT,
                             api_key=AZURE_OPENAI_API_KEY,
                             api_version=AZURE_OPENAI_API_VERSION
                             )
class Step(BaseModel):
    explanation: str
    output: str

class MathReasoning(BaseModel):
    steps: list[Step]
    final_answer: str
    famous_quote: str = Field(..., description="A famous quote that is not related to math.")

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
print("Quote:", math_reasoning.famous_quote)
