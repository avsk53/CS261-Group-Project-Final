from sqlalchemy import Column, String, Integer, DateTime, Float
from . import base

class Improvement_Metrics_Table(base):
  __tablename__ = 'improvement_metrics'

  metric_id = Column(Integer, primary_key=True)
  evaluation_id = Column(Integer, primary_key=True)
  direction = Column(Integer)
  improvement_value = Column(Float)
