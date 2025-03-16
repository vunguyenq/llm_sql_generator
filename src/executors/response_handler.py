from src.context.structured_output import SQLGeneration
import logging

def parse_structured_output_response(response: SQLGeneration) -> str:
    steps = response.steps
    logging.info("Reasoning steps:")
    for i, step in enumerate(steps):
        logging.info(f"\t{i}.{step}")
    return response.sql_query
