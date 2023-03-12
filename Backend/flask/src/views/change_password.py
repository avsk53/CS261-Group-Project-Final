from flask import request, jsonify
from . import views
from app import session, token_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import cross_origin # type: ignore
from sqlalchemy import select, update
from database import *


# Password change handler function
@views.route('/change_password', methods=['POST'])
@cross_origin()
@token_required
def change_password(auth_user):

    # Parse request data
    data = request.form
    token = data.get('server_token')
    user_id = data.get('user_id')
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if auth_user.user_id != int(user_id):
        response = jsonify({'message': 'You are not authorized to change this user\'s password', 'user_id': auth_user.user_id})
        status_code = 401
        return response, status_code

    # Query database for current password hash
    pwd = session.get(Passwords_Table, user_id)

    # Check if user exists and current password is correct
    if pwd is not None and check_password_hash(pwd.password_hash, current_password):

        # Update user's password hash with new password hash
        pwd.password_hash = generate_password_hash(new_password)
        session.commit()

        return jsonify({'message': 'Password changed successfully'})
    else:
        return jsonify({'message': 'Invalid username or current password'}), 402