from pydantic import BaseModel, Field
from typing import Optional
from port_service.dtos.request_dtos import CreatePortDTO
from environment_variable_service.dtos.request_dtos import CreateEnvironmentDTO
from volume_service.dtos.request_dtos import CreateVolumeDTO





class CreateWorkerDTO(BaseModel):
    docker_image: str = Field(None)
    parent_id: Optional[str] = Field(None)
    ports: list[CreatePortDTO] = Field(None)
    volumes: list[CreateVolumeDTO] = Field(None)
    environment: list[CreateEnvironmentDTO] = Field(None)
    # cpu_limit: float = Field(None)
    # memory_limit: float = Field(None)
    # gpu_limit: int = Field(None)
    # gpu_model: str = Field(None)
    # gpu_count: int = Field(None)
    # gpu_index: int = Field(None)