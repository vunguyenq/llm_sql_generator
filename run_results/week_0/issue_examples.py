import openai
import config
from src.executors.query_executor import create_system_context, format_user_prompt

OPENAI_API_KEY = config.OPEN_API_KEY

def query_open_ai(prompt: str, model: str = 'gpt-4o') -> str:
    """Sends a prompt to GPT-4 with structured roles."""
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"Error: {e}")
        return ""
    
if __name__ == "__main__":
    
    print('Issue 1: OpenAI API does not yet support session context. Have to send system context with each prompt => More input tokens.')
    query = "Which seller has delivered the most orders to customers in Rio de Janeiro? [string: seller_id]"
    messages=[
                {"role": "system", "content": create_system_context()},
                {"role": "user", "content": format_user_prompt(query)}
            ]
    for m in messages:
        print(f"Role: {m['role']}, Content: {m['content']}")
    
    print("\n--------------------------------\n")
    questions = ["What is the purpose of SELECT statement in SQL? Answer in one short sentence.",
                 "What was my last question?"]
    for question in questions:
        print(f"Question: {question}")
        response = query_open_ai(question)
        print(f"Response: {response}")
        print('\n--------------------------------')
        