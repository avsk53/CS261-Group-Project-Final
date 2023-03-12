from sqlalchemy import Column, String, Integer, DateTime
from . import base

class Team_Table(base):
  __tablename__ = 'teams'

  project_manager_id = Column(Integer, primary_key=True)
  supervisor_id = Column(Integer, primary_key=True)