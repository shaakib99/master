from database_service.mysql_service import MySQLDatabase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = MySQLDatabase.get_instance().base

class WorkerSchema(Base):
    __tablename__ = 'workers'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    status = Column(String(100))
    docker_image = Column(String(100))
    worker_ip = Column(String(100))
    root_password = Column(String(100))
    parent_id = Column(Integer, ForeignKey('workers.id'), nullable=True)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)