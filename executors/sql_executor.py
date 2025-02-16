import sqlite3
import logging
import pandas as pd

def query_db(query: str) -> pd.DataFrame:
    try:
        with sqlite3.connect('sqlitedb/olist.sqlite') as conn:
            df = pd.read_sql_query(query, conn)
            return df
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        return pd.DataFrame()  # Return an empty dataframe on error
