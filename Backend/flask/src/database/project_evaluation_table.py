from sqlalchemy import Column, String, Integer, DateTime
from . import base

class Project_Evaluation_Table(base):
  __tablename__ = 'project_evaluation'

  project_id = Column(Integer, primary_key=True)
  evaluation_id = Column(Integer, primary_key=True)
  evaluation_date = Column(DateTime)
  evaluation_type = Column(Integer)
  evaluation_label = Column(String)