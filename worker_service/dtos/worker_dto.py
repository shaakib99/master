from pydantic import BaseModel, Field
from typing import Optional


class WorkerDTO(BaseModel):
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    status: str = Field(None)
    docker_image: Optional[str] = Field(None)
    worker_ip: Optional[str] = Field(None)
    root_password: Optional[str] = Field(None, default='root')
    parent_id: Optional[str] = Field(None)
    created_at: Optional[str] = Field(None)
    updated_at: Optional[str] = Field(None)

    class Config:
        orm_mode = True
        allow_population_by_field_name = True