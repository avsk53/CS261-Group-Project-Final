from flask import request, jsonify
from . import views
from app import session, token_required
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import cross_origin # type: ignore
from database import *
from sqlalchemy import select, join

@views.route('/get_unassigned_pm', methods=['POST'])
@token_required
@cross_origin()
def get_unassigned_pm(auth_user):
    data = request.form
    supervisor_id = int(data.get('supervisor_id'))

    try:
        # Join the team and user tables
        joined = join(User_Table, Team_Table,
            User_Table.user_id == Team_Table.project_manager_id,
            full=True)
        
        # Get all PMs where supervisor_id matches
        blacklist = session.scalars(
            select(User_Table.user_id)
            .select_from(joined)
            .where(Team_Table.supervisor_id == supervisor_id)
            .where(User_Table.user_role == 2)
        ).all()

        # Get all PMs
        all_pms = session.scalars(
            select(User_Table)
            .where(User_Table.user_role == 2)
        )

        all_pms = list(filter(lambda pm: pm.user_id not in blacklist, all_pms))

        # Format the response
        response = [
            {
                "user_id": pm.user_id,
                "username": pm.username,
                "email": pm.email
            } for pm in all_pms
        ]

        return jsonify(response)

    except SQLAlchemyError as e:
        # handle the exception
        return jsonify({"message": "Could not get managers."}), 500
