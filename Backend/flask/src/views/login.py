from flask import request, jsonify
from . import views
from app import session, cfg
from werkzeug.security import check_password_hash
from database import *
from flask_cors import cross_origin # type: ignore
from sqlalchemy import select
import datetime
import jwt

# Password login handler function
@views.route('/login', methods=['POST'])
@cross_origin()
def login():
    # Parse request data
    data = request.json

    token = data.get('server_token')
    email = data.get('email')
    password = data.get('password')

    usr = session.scalar(
        select(User_Table)
        .filter_by(email=email)
    )

    # Check if user exists
    if usr is not None:
        # Query database for password hash
        pwd = session.get(Passwords_Table, usr.user_id)

        # Check if password hash matches
        if check_password_hash(pwd.password_hash, password):
            # Generate JWT token
            auth_token = jwt.encode({
              'public_id': usr.user_id,
              'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
              'iat' : datetime.datetime.utcnow()
            }, cfg['SECRET_KEY'])
            # return str(auth_token)
            # Return token and user data
            response = {
                'message': 'Login successful',
                'user' : {
                    'user_id': usr.user_id,
                    'username': usr.username,
                    'role_id': usr.user_role,
                    'role_desc': usr.role_desc, 
                    'email': usr.email,
                },
                'token': auth_token.decode()
            }
            return jsonify(response), 200

    return jsonify({'message': 'Invalid username or password'}), 401