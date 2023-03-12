from flask import request, jsonify
from . import views
from app import session, token_required
from sqlalchemy.exc import SQLAlchemyError
from flask_cors import cross_origin # type: ignore
from database import Team_Table

# assuming you receive a dictionary containing the user token and the supervisor id

@views.route('/unassign_pm', methods=['POST'])
@token_required
@cross_origin()
def unassign_pm(auth_user):
    data = request.form
    supervisor_id = int(data.get('supervisor_id'))
    project_manager_id = int(data.get('project_id'))

    try:
         # query for the record to delete
        team_record = session.query(Team_Table).filter_by(supervisor_id=supervisor_id, project_manager_id=project_manager_id).first()

        if team_record:
            # delete the record and commit the changes
            session.delete(team_record)
            session.commit()

            # return the deleted record as a dictionary
            return jsonify({
                "supervisor_id": supervisor_id,
                "project_manager_id": project_manager_id
            })

        else:
            # if the record doesn't exist, return None
            return jsonify({"message": "Assignment did not exist."}), 500

    except SQLAlchemyError as e:
        # handle the exception
        return jsonify({"message": "Removal failed."}), 500
    finally:
        # close the database connection
        session.close()
