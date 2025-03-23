from typing import NamedTuple


class FewShotExample(NamedTuple):
    prompt: str
    sql: str
    explanation: str = ""


FEW_SHOTS = [
    FewShotExample("Which seller has delivered the most orders to customers?",
                   "SELECT oi.seller_id FROM order_items oi GROUP BY oi.seller_id ORDER BY COUNT(DISTINCT oi.order_id) DESC LIMIT 1",
                   "When counting order_id from order_items, the count must be distinct"),
    FewShotExample("Which orders have items from multiple sellers?",
                   "SELECT order_id FROM order_items  GROUP BY order_id HAVING COUNT(DISTINCT seller_id) > 1",
                   "To get orders with multiple sellers, count distinct seller_id grouped by order_id. No need to join order_items to itself.")
]

def create_fewshots_assistant_answers() -> list[dict]:
    assistant_responses = []
    for example in FEW_SHOTS:
        assistant_responses.append({"role": "user", "content": example.prompt})
        assistant_responses.append({"role": "assistant", "content": example.sql})
    return assistant_responses
