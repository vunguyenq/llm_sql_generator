import re
from typing import NamedTuple
import sqlglot
import sqlparse

class HarmfulPattern(NamedTuple):
    pattern: str
    description: str


class HarmfulPatternException(Exception):
    def __init__(self, pattern_description: str):
        super().__init__(f"Query contains harmful pattern: {pattern_description}")

class InvalidQueryException(Exception):
    pass

def validate_sql(query: str):
    """Validate if the SQL query is syntactically correct using sqlglot."""
    try:
        sqlglot.parse_one(query, dialect="sqlite")
    except sqlglot.errors.ParseError as e:
        raise InvalidQueryException(f"SQL Syntax Error: {e}")

def format_sql_one_liner(query: str) -> str:
    """Format SQL into a one-liner."""
    return " ".join(sqlparse.format(query, reindent=True, keyword_case="upper").split())

def safety_check_sql(query: str) -> None:
    '''´Looks for harmful patterns in the SQL query.
    Raises HarmfulPatternException if a harmful pattern is found.'''

    harmful_patterns = [
        HarmfulPattern(r'(?i)\b(USE|SHOW|DESCRIBE|CALL|SET)\b', 'Database management queries'),
        HarmfulPattern(r'(?i)\b(DELETE|TRUNCATE|DROP)\s+TABLE', 'Table deletion queries'),
        HarmfulPattern(r'(?i)\b(DELETE|UPDATE|INSERT)\s+INTO', 'Data manipulation queries'),
        HarmfulPattern(r'(?i)\bCREATE\s+(DATABASE|SCHEMA|TABLE)', 'Database schema queries'),
        HarmfulPattern(r'(?i)\bGRANT|REVOKE', 'Permissions queries')
    ]

    for pattern in harmful_patterns:
        if re.search(pattern.pattern, query):
            raise HarmfulPatternException(pattern.description)

    return None
