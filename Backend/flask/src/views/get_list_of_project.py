from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session, token_required
from sqlalchemy import select
from database import *

def get_projects(user_id):
  # Get all PMs under the user if they're a supervisor
  manager_ids = session.scalars(
    select(Team_Table.project_manager_id)
    .filter_by(supervisor_id=user_id)
  ).all()
  manager_ids.append(user_id)

  # Get all projects that each PM owns
  projects = {}
  for id in manager_ids:
    manager_name = session.get(User_Table, id).username
    projects[manager_name] = session.scalars(select(Project_Table)
      .filter_by(project_manager_id=id)
    ).all()

  # Get the latest evaluations of each project
  for project_list in projects.values():
    for project in project_list:
      project.recent_evaluation = session.scalar(
        select(Project_Evaluation_Table)
        .where(Project_Evaluation_Table.project_id == project.project_id)
        .order_by(Project_Evaluation_Table.evaluation_date.desc())
        .limit(1)
      )

  # Return the list in the correct endpoint format
  output = []
  for manager in projects:
    for project in projects[manager]:
      output.append({
        "project_id": project.project_id,
        "project_name": project.project_name,
        "recent_evaluation_label": project.recent_evaluation.evaluation_label,
        "project_manager_name": manager
      })
  return output

@views.route("/get_list_of_project", methods=["POST"])
@cross_origin()
@token_required
def get_list_of_project(auth_user):
  if auth_user.user_role == 0 or auth_user.user_role == 3:
    return jsonify({'message': 'You are not authorized to access this endpoint'}), 401
  
  if request.method == "POST":

    user_id = request.form['user_id']
    token = request.form['server_token']

    output = get_projects(user_id)

  return jsonify(output)