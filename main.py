import logging

from src.context.structured_output import SQLGeneration
from src.executors.query_builder import create_query_message
from src.executors.query_executor import query_azure_open_ai
from src.executors.query_validator import (HarmfulPatternException,
                                           InvalidQueryException, pretify_sql,
                                           safety_check_sql, validate_sql)
from src.executors.response_handler import parse_structured_output_response
from src.executors.sql_executor import query_db
from src.utils.logging_utils import setup_logging

QUERIES = ['Which seller has delivered the most orders to customers in Rio de Janeiro?',
           "What's the average review score for products in the 'beleza_saude' category?",
           'How many sellers have completed orders worth more than 100,000 BRL in total?',
           'Which product category has the highest rate of 5-star reviews?',
           "What's the most common payment installment count for orders over 1000 BRL?",
           'Which city has the highest average freight value per order?',
           "What's the most expensive product category based on average price?",
           'Which product category has the shortest average delivery time?',
           'How many orders have items from multiple sellers?',
           'What percentage of orders are delivered before the estimated delivery date?'
           ]

def send_user_query(question: str) -> str:
    logging.info("")
    logging.info(f"Executing query: {question}")
    response = query_azure_open_ai(messages=create_query_message(question), response_format=SQLGeneration, log=True)
    sql_query = parse_structured_output_response(response)
    logging.info(f"SQL query: \n{pretify_sql(sql_query)}")
    return sql_query

def format_and_validate_sql(sql_query: str) -> str:
    try:
        safety_check_sql(sql_query)
        validate_sql(sql_query)
    except (InvalidQueryException, HarmfulPatternException) as e:
        logging.error(f"Query validation failed: {e}")
    # return format_sql_one_liner(sql_query)
    return sql_query


if __name__ == "__main__":
    setup_logging(console=False)
    for i, question in enumerate(QUERIES):
        print('\n-----------------------------------\n')
        print(f"Executing query: {i+1}. {question}")
        sql_query = send_user_query(question)
        sql_query = format_and_validate_sql(sql_query)
        print("SQL query:", pretify_sql(sql_query))
        print("Query result:")
        print(query_db(sql_query))
