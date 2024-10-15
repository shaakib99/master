import asyncio
import subprocess

class CommandService:
    def __init__(self):
        pass

    async def execute(self, command: str):
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            return stdout.decode().strip()
        else:
            return f"Error: {stderr.decode().strip()}"

