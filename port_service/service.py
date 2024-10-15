from database_service.service import DatabaseService
from port_service.schemas.port_schema import PortSchema
from port_service.dtos.request_dtos import CreatePortDTO
from port_service.dtos.port_dto import PortDTO
from common.exceptions import NotFoundException
from database_service.dtos.query_param_dto import SQLQueryParamDTO
import socket

class PortService:
    def __init__(self, port_model = DatabaseService[PortSchema](PortSchema)):
        self.port_model = port_model
    
    async def create_one(self, data: CreatePortDTO):
        port_dto = PortDTO
        port_dto.worker_id = data.worker_id
        port_dto.port = data.port
        port_dto.mapped_port = self.get_free_port()
        port_dto.should_add_to_load_balancer = data.should_add_to_load_balancer
        return await self.port_model.save_one(data)

    async def get_one(self, port_id: str):
        port = await self.port_model.get_one(port_id)
        if port is None:
            raise NotFoundException('Port not found')
        return port

    async def get_all(self, query: SQLQueryParamDTO):
        return await self.port_model.get_all(query)

    async def delete_one(self, port_id: str):
        port = await self.port_model.get_one(port_id)
        if port is None:
            raise NotFoundException('Port not found')
        await self.port_model.delete_one(port_id)
    

    async def get_free_port(self) -> int:
        sock = socket.socket()
        sock.bind(('', 0))
        port = sock.getsockname()[1]
        sock.close()
        return port