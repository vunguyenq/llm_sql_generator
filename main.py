import logging

from src.executors.query_executor import (extract_sql_from_response,
                                          query_open_ai)
from src.executors.query_validator import (HarmfulPatternException,
                                           InvalidQueryException,
                                           format_sql_one_liner,
                                           safety_check_sql, validate_sql)
from src.executors.sql_executor import query_db
from src.utils.logging_utils import setup_logging

QUERIES = ['Which seller has delivered the most orders to customers in Rio de Janeiro? [string: seller_id]',
           "What's the average review score for products in the 'beleza_saude' category? [float: score]",
           'How many sellers have completed orders worth more than 100,000 BRL in total? [integer: count]',
           'Which product category has the highest rate of 5-star reviews? [string: category_name]',
           "What's the most common payment installment count for orders over 1000 BRL? [integer: installments]",
           'Which city has the highest average freight value per order? [string: city_name]',
           "What's the most expensive product category based on average price? [string: category_name]",
           'Which product category has the shortest average delivery time? [string: category_name]',
           'How many orders have items from multiple sellers? [integer: count]',
           'What percentage of orders are delivered before the estimated delivery date? [float: percentage]'
           ]

def format_and_validate_sql(response: str) -> str:
    sql_query = extract_sql_from_response(response)
    try:
        safety_check_sql(sql_query)
        validate_sql(sql_query)
    except (InvalidQueryException, HarmfulPatternException) as e:
        logging.error(f"Query validation failed: {e}")
    # return format_sql_one_liner(sql_query)
    return sql_query


if __name__ == "__main__":
    setup_logging()
    for i, query in enumerate(QUERIES[:2]):
        print('\n-----------------------------------\n')
        print(f"Executing query: {i+1}. {query}")
        response = query_open_ai(query)
        sql_query = format_and_validate_sql(response)
        print("SQL query:", sql_query)
        print("Query result:")
        print(query_db(sql_query))
