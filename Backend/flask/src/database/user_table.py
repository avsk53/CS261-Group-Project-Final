from sqlalchemy import Column, String, Integer, DateTime
from . import base

class User_Table(base):
  __tablename__ = 'users'

  user_id = Column(Integer, primary_key=True)
  username = Column(String)
  user_role = Column(Integer)
  role_desc = Column(String)
  email = Column(String)
  last_logged_in = Column(DateTime)