from sqlalchemy import Column, String, Integer, DateTime
from . import base

class Project_Table(base):
  __tablename__ = 'project'

  project_id = Column(Integer, primary_key=True)
  project_name = Column(String)
  project_start = Column(DateTime)
  project_end = Column(DateTime)
  number_of_people = Column(Integer)
  github_link = Column(String)
  project_manager_id = Column(Integer)