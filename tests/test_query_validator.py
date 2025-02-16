import pytest
import sys
import os
# Add the root folder to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from executors.query_validator import safety_check_sql

from executors.query_validator import safety_check_sql, HarmfulPatternException

def test_safety_check_sql_no_harmful_patterns():
    query = "SELECT * FROM users WHERE id = 1"
    assert safety_check_sql(query) is None

def test_safety_check_sql_database_management_queries():
    query = "USE my_database"
    with pytest.raises(HarmfulPatternException, match="Database management queries"):
        safety_check_sql(query)

def test_safety_check_sql_table_deletion_queries():
    query = "DROP TABLE users"
    with pytest.raises(HarmfulPatternException, match="Table deletion queries"):
        safety_check_sql(query)

def test_safety_check_sql_data_manipulation_queries():
    query = "INSERT INTO users (id, name) VALUES (1, 'John')"
    with pytest.raises(HarmfulPatternException, match="Data manipulation queries"):
        safety_check_sql(query)

def test_safety_check_sql_database_schema_queries():
    query = "CREATE TABLE users (id INT, name VARCHAR(100))"
    with pytest.raises(HarmfulPatternException, match="Database schema queries"):
        safety_check_sql(query)

def test_safety_check_sql_permissions_queries():
    query = "GRANT ALL PRIVILEGES ON database TO user"
    with pytest.raises(HarmfulPatternException, match="Permissions queries"):
        safety_check_sql(query)
