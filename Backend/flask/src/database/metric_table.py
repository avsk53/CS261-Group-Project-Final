from sqlalchemy import Column, String, Integer, DateTime
from . import base

class Metric_Table(base):
  __tablename__ = 'metric'

  metric_id = Column(Integer, primary_key=True)
  metric_type = Column(Integer)
  metric_desc = Column(String)