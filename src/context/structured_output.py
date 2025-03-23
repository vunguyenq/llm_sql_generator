from pydantic import BaseModel, Field, conlist

class SQLGeneration(BaseModel):
    # steps: conlist(str, max_length=3) = Field(..., description="Short chain-of-thought steps explaining the logic. Include SQL sub-query in each step.")  # Conlist is not supported
    steps: list[str] = Field(..., description="Short chain-of-thought steps explaining the logic. Include SQL sub-query in each step. Maximum 3 steps.")
    sql_query: str = Field(..., description="The final SQL query to answer the user request in SQLite syntax.")
