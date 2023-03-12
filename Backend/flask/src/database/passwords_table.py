from sqlalchemy import Column, String, Integer
from . import base

class Passwords_Table(base):
  __tablename__ = 'passwords'

  user_id = Column(Integer, primary_key=True)
  password_hash = Column(String)