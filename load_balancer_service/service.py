from command_service.service import CommandService
from worker_service.dtos.worker_dto import WorkerDTO

class LoadBalancerService:
    def __init__(self, command_service: CommandService):
        self.command_service = command_service

    async def add_upstream(self, worker: WorkerDTO, should_reload_nginx = False):
        # remove all ports that should not be added to load balanc
        await self.remove_upstream(worker)

        # add all ports that should be added to load balancer
        for port in worker.ports:
            if port.should_add_to_load_balancer:
                command = f"ansible-playbook -i ./ansible_playbooks/add_upstream.ansible.yml --extra-vars 'new_host={worker.worker_ip}:{port.mapped_port}'"
                await self.command_service.execute(command)

        if should_reload_nginx:
            await self.reload_nginx(worker)
    
    async def remove_upstream(self, worker: WorkerDTO, should_reload_nginx = False):
        for port in worker.ports:
            if port.should_add_to_load_balancer:
                command = f"ansible-playbook -i ./ansible_playbooks/remove_upstream.ansible.yml --extra-vars 'target={worker.worker_ip}:{port.mapped_port}'"
                await self.command_service.execute(command)

        if should_reload_nginx:
            await self.reload_nginx(worker)

    async def reload_nginx(self, worker: WorkerDTO):
        command = "ansible-playbook -i ./ansible_playbooks/reload_nginx.ansible.yml"
        await self.command_service.execute(command)
