from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session
from sqlalchemy import select, insert, text
from database import *
from datetime import datetime
from werkzeug.security import generate_password_hash

@views.route("/")
def index():

  # # Insert a new value
  # session.execute(
  #   insert(User_Table).values(
  #     user_id=2151141,
  #     username="J-Burnham",
  #     user_role=0,
  #     role_desc="admin",
  #     email="James.Burnham@warwick.ac.uk",
  #     last_logged_in=datetime.now()
  #   )
  # )

  # # Commit the change
  # session.commit()

  # Read the value we committed
  # user = session.get(User_Table, 2151141)

  record = session.execute(text("SELECT * from testview;")).mappings().all()

  return jsonify(f"{record}")