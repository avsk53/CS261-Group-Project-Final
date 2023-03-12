from flask import request, jsonify
from . import views
from app import session, token_required
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import cross_origin # type: ignore
from database import Team_Table

# assuming you receive a dictionary containing the user token and the supervisor id

@views.route('/assign_pm', methods=['POST'])
@token_required
@cross_origin()
def assign_pm(auth_user):
    data = request.form
    supervisor_id = int(data.get('supervisor_id'))
    project_manager_id = int(data.get('project_id'))

    try:
        # create a new TeamTable object with the given values
        team_record = Team_Table(supervisor_id=supervisor_id, project_manager_id=project_manager_id)

        # add the object to the session and commit the changes
        session.add(team_record)
        session.commit()

        # return the inserted record as a dictionary
        return jsonify({
            "supervisor_id": supervisor_id,
            "project_manager_id": project_manager_id
        })

    except SQLAlchemyError as e:
        # handle the exception
        return jsonify({"message": "Assignment already exists."})
    finally:
        # close the database connection
        session.close()
