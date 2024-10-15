from volume_service.schemas.volume_schema import VolumeSchema
from volume_service.dtos.request_dtos import CreateVolumeDTO
from volume_service.dtos.volume_dto import VolumeDTO
from common.exceptions import NotFoundException
from database_service.service import DatabaseService
from database_service.dtos.query_param_dto import SQLQueryParamDTO


class VolumeService:
    def __init__(self, volume_model = DatabaseService[VolumeSchema](VolumeSchema)):
        self.volume_model = volume_model

    async def create_one(self, data: CreateVolumeDTO):
        volume_dto = VolumeDTO()
        volume_dto.name = data.name
        volume_dto.path = data.path
        volume_dto.worker_id = data.worker_id
        return await self.volume_model.create_one(data)

    async def get_one(self, volume_id: str):
        volume = await self.volume_model.get_one(volume_id)
        if not volume:
            raise NotFoundException('Volume not found')
        return volume

    async def get_all(self, query_param: SQLQueryParamDTO):
        return await self.volume_model.get_all(query_param)

    async def delete_one(self, volume_id: str):
        await self.volume_model.get_one(volume_id)