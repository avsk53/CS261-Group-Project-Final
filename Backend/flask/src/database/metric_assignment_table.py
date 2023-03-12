from sqlalchemy import Column, String, Integer, DateTime, Float
from . import base

class Metric_Assignment_Table(base):
  __tablename__ = 'metric_assignment'

  metric_id = Column(Integer, primary_key=True)
  project_id = Column(Integer, primary_key=True)
  metric_value = Column(Float)
