from flask import request, jsonify
from . import views
from app import session, token_required
from database import *
from flask_cors import cross_origin # type: ignore
from sqlalchemy import update

# Updates the start or end date of a project
@views.route('/update_project_info', methods=['POST'])
@cross_origin()
@token_required
def update_project_info(auth_user):
    # Parse request data
    data = request.json

    token = data.get('server_token')
    project_id = data.get('project_id')
    attribute = data.get('attribute')
    new_val = data.get('new_value')

    if attribute == "start_date":
        session.execute(
            update(Project_Table)
            .where(Project_Table.project_id == project_id)
            .values(project_start=new_val)
        )
    elif attribute == "end_date":
        session.execute(
            update(Project_Table)
            .where(Project_Table.project_id == project_id)
            .values(project_end=new_val)
        )
    else:
        return jsonify({'message': 'Invalid attribute.'}), 401
    session.commit()

    project = session.get(Project_Table, project_id)
    start = project.project_start
    end = project.project_end

    months_allocated = (end.year - start.year) * 12 + end.month - start.month
    session.execute(
        update(Metric_Assignment_Table)
        .filter_by(project_id=project_id)
        .filter_by(metric_id=15)
        .values(metric_value=months_allocated)
    )


    return jsonify({'message': 'Project updated.'}), 200
