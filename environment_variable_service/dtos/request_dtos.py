from pydantic import BaseModel, Field
from typing import Optional

class CreateEnvironmentDTO(BaseModel):
    worker_id: Optional[str] = Field(None)
    name: str = Field(None)
    value: str = Field(None)