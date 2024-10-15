from command_service.service import CommandService

class DockerService:
    def __init__(self, command_service: CommandService):
        self.command_service = command_service

    async def run_container(self, image_name: str, container_name: str, port_mapping: list[str], env_vars: list[str], volumes: list[str]):
        command = f"docker run -d --name {container_name} {image_name}"

        for port_map in port_mapping:
            command += f" -p {port_map}"
        
        for env in env_vars:
            command += f" -e {env}"
        
        for volume in volumes:
            command += f" -v {volume}"
        
        await self.command_service.execute(command)
    
    async def stop_container(self, container_name: str):
        command = f"docker stop {container_name}"
        await self.command_service.execute(command)
    
    async def remove_container(self, container_name: str):
        command = f"docker rm {container_name}"
        await self.command_service.execute(command)
