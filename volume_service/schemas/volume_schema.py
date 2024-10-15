from database_service.mysql_service import MySQLDatabase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = MySQLDatabase.get_instance().base

class VolumeSchema(Base):
    __tablename__ = 'volumes'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    path = Column(String(100))
    worker_id = Column(Integer, ForeignKey('workers.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)