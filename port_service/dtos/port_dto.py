from pydantic import BaseModel, Field
from typing import Optional

class PortDTO(BaseModel):
    port: Optional[int] = Field(None, description="port")
    mapped_port: Optional[int] = Field(None, description="mapped_port")
    should_add_to_load_balancer: Optional[bool] = Field(None, description="should_add_to_load_balancer")
    worker_id: Optional[str] = Field(None, description="worker_id")


    class Config:
        orm_mode = True
        allow_population_by_field_name = True