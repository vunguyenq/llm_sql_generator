import openai
import config

OPENAI_API_KEY = config.API_KEY

def query_open_ai(prompt: str, model:str = 'gpt-4o') -> str:
    """Sends a prompt to GPT-4 with structured roles."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are an expert SQL assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
            print(f"Error: {e}")
            return ""
