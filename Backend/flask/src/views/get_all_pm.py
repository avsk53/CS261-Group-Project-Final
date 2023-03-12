from flask import request, jsonify
from . import views
from app import session, token_required
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import cross_origin # type: ignore
from database import *
from sqlalchemy import select, join


# assuming you receive a dictionary containing the user token and the desired supervisor id

@views.route('/get_all_pm', methods=['POST'])
@cross_origin()
@token_required
def get_all_pm(auth_user):
    data = request.form
    supervisor_id = data.get('supervisor_id')

    try:
        joined = join(Team_Table, User_Table,
                Team_Table.project_manager_id == User_Table.user_id)

        # retrieve the project managers that are assigned to the passed in id
        pms = session.scalars(
            select(User_Table)
            .select_from(joined)
            .where(Team_Table.supervisor_id == supervisor_id)
        ).all()

        response = [{
            "user_id": pm.user_id,
            "username": pm.username,
            "email": pm.email
        } for pm in pms]

        return jsonify(response)

    except SQLAlchemyError as e:
        # handle the exception
        return jsonify({"message": "Could not fetch managers."}), 500
    finally:
        # close the database connection
        session.close()
