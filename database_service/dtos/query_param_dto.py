from pydantic import BaseModel, Field
from fastapi import Query
from typing import Optional

class SQLQueryParamDTO(BaseModel):
    limit: int = 10
    skip: int = 0
    order_by: Optional[str] = None
    group_by: Optional[str] = None
    having: Optional[str] = None
    selected_fields: Optional[list[str]] = Field(Query([]))
    join: Optional[list[str]] = Field(Query([]))
    filter_by: Optional[str] = None