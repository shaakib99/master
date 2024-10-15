from pydantic import BaseModel, Field
from typing import Optional

class CreatePortDTO(BaseModel):
    worker_id: Optional[str] = Field(None)
    port: int = Field(None)
    should_add_to_load_balancer: Optional[bool] = Field(None)