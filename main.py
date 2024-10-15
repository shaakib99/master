from fastapi import FastAPI, APIRouter
from worker_service.route import router as worker_router
from database_service.service import DatabaseService
from dotenv import load_dotenv

async def lifespan(app):
    load_dotenv()
    database_service = DatabaseService(None)
    database_service.connect()
    yield
    database_service.disconnect()

app = FastAPI()

routers: list[APIRouter] = [worker_router]

for router in routers:
    app.include_router(router)