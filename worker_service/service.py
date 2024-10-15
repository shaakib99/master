from database_service.service import DatabaseService
from worker_service.dtos.request_dtos import CreateWorkerDTO, CreatePortDTO, CreateEnvironmentDTO
from worker_service.dtos.worker_dto import WorkerDTO
from port_service.dtos.port_dto import PortDTO
from environment_variable_service.dtos.environment_dto import EnvironmentDTO
from volume_service.dtos.volume_dto import VolumeDTO
from port_service.schemas.port_schema import PortSchema
from volume_service.schemas.volume_schema import VolumeSchema
from environment_variable_service.schemas.enviroment_schema import EnviromentSchema
from worker_service.schemas.worker_schema import WorkerSchema
from docker_service.service import DockerService
from port_service.service import PortService
from volume_service.service import VolumeService
from environment_variable_service.service import EnvironmentVariableService
from load_balancer_service.service import LoadBalancerService
from database_service.dtos.query_param_dto import SQLQueryParamDTO
from common.exceptions import NotFoundException
from common.enums import CONTAINER_STATUS
from uuid import uuid4

class WorkerService:
    def __init__(self, 
                 worker_model = DatabaseService[WorkerSchema](WorkerSchema), 
                 port_service = PortService(),
                 environment_variable_service = EnvironmentVariableService(),
                 volume_service = VolumeService(),
                 docker_service = DockerService(),
                 load_balancer_service = LoadBalancerService()):
        self.worker_model = worker_model
        self.port_service = port_service
        self.environment_variable_service = environment_variable_service
        self.volume_service = volume_service
        self.docker_service = docker_service
        self.load_balancer_service = load_balancer_service

    async def create_one(self, data: CreateWorkerDTO):
        worker_dto = WorkerDTO()
        worker_dto.name = uuid4().__str__()
        worker_dto.worker_ip = 'localhost'
        worker_dto.root_password = 'root'
        worker_dto.docker_image = data.docker_image
        worker_dto.status = CONTAINER_STATUS.INIT
        worker_dto.parent_id = data.parent_id

        worker = await self.worker_model.save_one(worker_dto)

        port_schemas: list[PortSchema] = []

        # default ssh port
        ssh_port = CreatePortDTO(port=22, should_add_to_load_balancer=False)

        all_ports = [*data.ports, CreatePortDTO(port=6969, should_add_to_load_balancer=False)]

        # If this is not a clone, then add the ssh port
        if data.parent_id is None:
            all_ports.append(ssh_port)

        for port in all_ports:
            port_dto = PortDTO()
            port_dto.port = port.port
            port_dto.mapped_port = self.port_service.get_free_port()
            port_dto.worker_id = worker.id
            port_dto.should_add_to_load_balancer = port.should_add_to_load_balancer

            result = await self.port_service.save_one(port_dto, worker.id)
            port_schemas.append(result)

        environment_schemas: list[EnviromentSchema] = []
        for env in [*data.environment, 
                    CreateEnvironmentDTO(name='WORKER_IP', value='localhost'), 
                    CreateEnvironmentDTO(name='WORKER_ID', value=worker.name)]:
            environment_dto = EnvironmentDTO()
            environment_dto.name = env.name
            environment_dto.value = env.value
            environment_dto.worker_id = worker.id

            result = await self.environment_variable_service.save_one(env, worker.id)
            environment_schemas.append(result)

        volume_schemas: list[VolumeSchema] = []
        for volume in data.volumes:
            volume_dto = VolumeDTO()
            volume_dto.name = volume.name
            volume_dto.path = volume.path
            volume_dto.worker_id = worker.id

            result = await self.volume_service.save_one(volume, worker.id)
            volume_schemas.append(result)
        
    
        await self.docker_service.run_container(
            data.docker_image, 
            worker_dto.name, 
            [f"{port.mapped_port}:{port.port}" for port in port_schemas], 
            [f"{env.name}={env.value}" for env in environment_schemas], 
            [f"{volume.name}:{volume.path}" for volume in volume_schemas])

        worker_dto.status = CONTAINER_STATUS.RUNNING
        await self.worker_model.update_one(worker.id, worker_dto)

        worker_dto = WorkerDTO.model_validate(worker)

        for port in port_schemas:
            if port.should_add_to_load_balancer:
                await self.load_balancer_service.add_upstream(worker = worker_dto, should_reload_nginx=False)
            
        await self.load_balancer_service.reload_nginx(worker = worker_dto)

        return worker

    async def get_one(self, worker_id: str):
        worker = await self.worker_model.get_one(worker_id)
        if worker is None:
            raise NotFoundException('Worker not found')
        return worker

    async def get_all(self, query: SQLQueryParamDTO):
        return await self.worker_model.get_all(query)

    async def delete_one(self, worker_id: str):
        worker = await self.worker_model.get_one(worker_id)
        if worker is None:
            raise NotFoundException('Worker not found')

        await self.docker_service.stop_container(worker.name)
        await self.docker_service.remove_container(worker.name)
        await self.load_balancer_service.remove_upstream(worker)

        await self.worker_model.delete_one(worker_id)