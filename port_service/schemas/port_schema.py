from database_service.mysql_service import MySQLDatabase
from sqlalchemy import Column, Integer, DateTime, Boolean, ForeignKey

Base = MySQLDatabase.get_instance().base

class PortSchema(Base):
    __tablename__ = 'ports'

    id = Column(Integer, primary_key=True)
    port = Column(Integer)
    mapped_port = Column(Integer)
    should_add_to_load_balancer = Column(Boolean)
    worker_id = Column(Integer, ForeignKey('workers.id'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)