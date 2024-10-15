from database_service.service import DatabaseService
from environment_variable_service.schemas.enviroment_schema import EnviromentSchema
from environment_variable_service.dtos.request_dtos import CreateEnvironmentDTO
from environment_variable_service.dtos.environment_dto import EnvironmentDTO
from common.exceptions import NotFoundException
from database_service.dtos.query_param_dto import SQLQueryParamDTO


class EnvironmentVariableService:
    def __init__(self, environment_model = DatabaseService(EnviromentSchema)):
        self.environment_model = environment_model

    async def create_one(self, data: CreateEnvironmentDTO):
        environment_variable = EnvironmentDTO()
        environment_variable.name = data.name
        environment_variable.value = data.value
        environment_variable.worker_id = data.worker_id
        return await self.environment_model.create_one(environment_variable)

    async def get_one(self, environment_id: str):
        environment = await self.environment_model.get_one(environment_id)
        if environment is None:
            raise NotFoundException('Environment not found')

        return environment

    async def get_all(self, query_param: SQLQueryParamDTO):
        return await self.environment_model.get_all(query_param)
    
    async def delete_one(self, environment_id: str):
        await self.environment_model.get_one(environment_id)
        await self.environment_model.delete_one(environment_id)