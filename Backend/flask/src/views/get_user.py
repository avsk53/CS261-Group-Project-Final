from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session, token_required
from sqlalchemy import select
from database import *

@views.route("/get_user", methods=["GET"])
@cross_origin()
@token_required
def get_user(auth_user):
  
  if request.method == "GET":
    usr = session.scalar(select(User_Table).where(User_Table.user_id == auth_user.user_id))

    output = {
        "user_id": usr.user_id,
        "username": usr.username,
        "user_role": usr.user_role,
        "role_desc": usr.role_desc,
        
    }
  return jsonify(output), 200