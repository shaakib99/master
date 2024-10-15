from pydantic import BaseModel, Field
from typing import Optional

class CreateVolumeDTO(BaseModel):
    worker_id: Optional[str] = Field(None)
    name: str = Field(None)
    path: str = Field(None)