from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session, token_required
from sqlalchemy import insert, select
from database import *
from datetime import datetime

@views.route("/create_developer", methods=["POST"])
@cross_origin()
@token_required
def create_developer(auth_user):
  if request.method == "POST":
    data = request.get_json()

    token = data["server_token"]
    username = data["username"]
    email = data["email"]

    try:
      #Check to make sure that a user with the same email does not already exist
      search =  session.scalar(select(User_Table).filter_by(email=email).limit(1))
      if search is not None:
        response = {"message": 'A user with that email already exists.'}
        code = 402
        return jsonify(response), code
    except Exception as e:
      response = {"message": '1st Error User could not be created.'}
      code = 500
      return jsonify(response), code

    try:
      # Insert the user using the information given
      user_id = session.execute(
        insert(User_Table).values(
          username=username,
          user_role=3,
          role_desc="Developer",
          email=email,
          last_logged_in=datetime.now()
        )
      ).inserted_primary_key[0]
      
      session.commit()
      response = {"message": 'User successfully created.',
                  "user_id": user_id}
      code = 200  
    except:
      response = {"message": 'User could not be created.'}
      code = 500

    return jsonify(response), code
