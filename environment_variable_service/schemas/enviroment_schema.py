from database_service.mysql_service import MySQLDatabase
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey

Base = MySQLDatabase.get_instance().base

class EnviromentSchema(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    value = Column(String(100))
    worker_id = Column(Integer, ForeignKey('workers.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)