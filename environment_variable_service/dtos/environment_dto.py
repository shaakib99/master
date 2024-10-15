from pydantic import BaseModel, Field
from typing import Optional

class EnvironmentDTO(BaseModel):
    name: Optional[str] = Field(None)
    value: Optional[str] = Field(None)
    worker_id: Optional[str] = Field(None)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True