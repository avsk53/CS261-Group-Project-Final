from sqlalchemy import Column, String, Integer, DateTime
from . import base

class Project_Assignment_Table(base):
  __tablename__ = 'project_assignments'

  user_id = Column(Integer, primary_key=True)
  project_id = Column(Integer, primary_key=True)