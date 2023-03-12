from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session, token_required
from sqlalchemy import insert, select
from database import *
from datetime import datetime
from werkzeug.security import generate_password_hash

@views.route("/create_user_account", methods=["POST"])
@cross_origin()
@token_required
def create_user_account(auth_user):
  # Ensure only system administrators can create accounts
  if auth_user.user_role != 0:
    return jsonify({'message': 'You are not authorized to access this endpoint', "user" : auth_user}), 401

  if request.method == "POST":
    data = request.get_json()

    token = data["server_token"]
    username = data["username_created"]
    user_role = int(data["user_role_created"])
    email = data["email_created"]
    password = data["password_created"]

    password_hash = generate_password_hash(password)

    roles = ["Admin", "Supervisor", "Project Manager", "Developer"]

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
          user_role=user_role,
          role_desc=roles[user_role],
          email=email,
          last_logged_in=datetime.now()
        )
      ).inserted_primary_key[0]

      # Insert their password
      session.execute(
        insert(Passwords_Table).values(
          user_id=user_id,
          password_hash=password_hash
        )
      )
      
      session.commit()
      response = {"message": 'User successfully created.',
                  "user_id": user_id}
      code = 200  
    except:
      response = {"message": 'User could not be created.'}
      code = 500

    return jsonify(response), code
