from database_service.lib.db_abc import DatabaseABC
from database_service.mysql_service import MySQLDatabase
from typing import Generic, TypeVar
import asyncio

T = TypeVar("T")

# TODO: Need fix typing for crud ops

class DatabaseService(Generic[T]):
    def __init__(self, schema, Service: DatabaseABC = MySQLDatabase):
        self.service = Service.get_instance()
        self.schema = schema
    
    async def connect(self):
        await asyncio.to_thread(self.service.connect())
    
    async def disconnect(self):
        await asyncio.to_thread(self.service.disconnect())
    
    async def create_metadata(self):
        await asyncio.to_thread(self.service.create_metadata())
    
    async def get_one(self, id: int) -> T:
        return await asyncio.to_thread(self.service.getOneById(self.schema, id))

    async def get_all(self, query) -> list[T]:
        return await asyncio.to_thread(self.service.getAll(self.schema, query))
    
    async def save_one(self, data: dict) -> T:
        return await asyncio.to_thread(self.service.saveOne(self.schema, data))
    
    async def update_one(self, id: str, data: dict) -> T:
        return await asyncio.to_thread(self.service.updateOne(self.schema, id, data))
    
    async def delete_one(self, id: str) -> None:
        return await asyncio.to_thread(self.service.deleteOne(self.schema, id))