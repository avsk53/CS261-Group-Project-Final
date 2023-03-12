from flask import request, jsonify
from . import views
from app import session, token_required
from database import *
from flask_cors import cross_origin # type: ignore
from sqlalchemy import update
from datetime import datetime

# Logout handler function
@views.route('/logout', methods=['POST'])
@cross_origin()
@token_required
def logout(auth_user):
    # Parse request data
    data = request.json
    token = data.get('server_token')
    
    user = session.get(User_Table, auth_user.user_id)

    now = datetime.now()
    diff = (now - user.last_logged_in).days

    # Update last_logged_in if it's been a week
    if diff >= 7:
        session.execute(
            update(User_Table)
            .where(User_Table.user_id == auth_user.user_id)
            .values(last_logged_in="now")
        )
        session.commit()

    return jsonify({'message': 'User logged out.'}), 200
