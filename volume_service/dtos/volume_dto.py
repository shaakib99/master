from pydantic import BaseModel, Field
from typing import Optional

class VolumeDTO(BaseModel):
    name: str = Field(..., description="Name of the volume")
    path: str = Field(..., description="Path of the volume")
    worker_id: Optional[str] = Field(None, description="Worker ID")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True