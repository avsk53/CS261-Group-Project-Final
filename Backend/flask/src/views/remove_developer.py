from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session, token_required
from sqlalchemy import delete, update, select
from database import *

@views.route("/remove_developer", methods=["POST"])
@cross_origin()
@token_required
def remove_developer(auth_user):
  if request.method == "POST":
    data = request.get_json()

    token = data["server_token"]
    user_id = data.get("user_id")
    project_id = data["project_id"]

    try:

      # Ensure that they are assigned
      assignment = session.get(Project_Assignment_Table, {
        "project_id": project_id,
        "user_id": user_id
      })

      if assignment is None:
        return jsonify({"message": "Developer already unassigned."}), 400

      # Remove the developer from the project
      session.execute(
        delete(Project_Assignment_Table)
        .where(Project_Assignment_Table.project_id == project_id)
        .where(Project_Assignment_Table.user_id == user_id)
      )

      # Decrease the number of people by 1
      project = session.get(Project_Table, project_id)
      session.execute(
        update(Project_Table)
        .where(Project_Table.project_id == project_id)
        .values(number_of_people=(project.number_of_people-1))
      )

      session.execute(
        update(Metric_Assignment_Table)
        .where(Metric_Assignment_Table.project_id == project_id)
        .where(Metric_Assignment_Table.metric_id == 2)
        .values(metric_value=(Metric_Assignment_Table.metric_value-1))
      )
      session.commit()
      team_members = session.scalars(
          select(User_Table)
          .join(Project_Assignment_Table, User_Table.user_id == Project_Assignment_Table.user_id)
          .filter(Project_Assignment_Table.project_id == project.project_id)
          .order_by(User_Table.user_id)
      ).all()

      response = {
        "message": 'Developer removed successfully.', 
        "team_members": [
          {
				    "username": t.username,
            "user_id": t.user_id,
            "email": t.email,
            "role": t.role_desc
				  } for t in team_members
        ]
      }
      code = 200  
    except:
      response = {"message": 'Developer could not be removed.'}
      code = 500

    return jsonify(response), code
