from worker_service.service import WorkerService
from common.exceptions import NotFoundException, BadRequestException
from port_service.service import PortService
from environment_variable_service.service import EnvironmentVariableService
from volume_service.service import VolumeService
from database_service.dtos.query_param_dto import SQLQueryParamDTO
from worker_service.dtos.request_dtos import CreateWorkerDTO

class PrometheusService:
    def __init__(self, 
                 worker_service = WorkerService(),
                 port_service = PortService(),
                 environment_variable_service = EnvironmentVariableService(),
                 volume_service = VolumeService()) -> None:
        self.worker_service = worker_service
        self.port_service = port_service
        self.environment_variable_service = environment_variable_service
        self.volume_service = volume_service
    
    async def create_new_instance(self, worker_id: str):
        worker = await self.worker_service.get_one(worker_id)

        if worker is None:
            raise NotFoundException('Worker not found')

        query_param_dto = SQLQueryParamDTO()
        query_param_dto.filter_by = f'worker_id = \'{worker_id}\''

        ports = await self.port_service.get_all(query_param_dto)
        environment_variables = await self.environment_variable_service.get_all(query_param_dto)
        volumes = await self.volume_service.get_all(query_param_dto)
    
        create_worker_dto = CreateWorkerDTO()
        create_worker_dto.docker_image = worker.docker_image
        create_worker_dto.ports = ports
        create_worker_dto.environment_variables = environment_variables
        create_worker_dto.volumes = volumes
        create_worker_dto.parent = worker.id

    async def remove_instance(self, worker_id: str):
        worker = await self.worker_service.get_one(worker_id)
        if worker is None:
            raise NotFoundException('Worker not found')

        if worker.parent is not None:
            raise BadRequestException('Cannot delete a cloned worker')
        
        await self.worker_service.delete_one(worker_id)