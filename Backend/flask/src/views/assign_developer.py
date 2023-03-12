from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session, token_required
from sqlalchemy import insert, update, select
from database import *

@views.route("/assign_developer", methods=["POST"])
@cross_origin()
@token_required
def assign_developer(auth_user):
  if request.method == "POST":
    data = request.get_json()

    token = data["server_token"]
    user_id = data.get("user_id")
    project_id = data["project_id"]

    try:
      # Ensure that they are not already assigned
      assignment = session.get(Project_Assignment_Table, {
        "project_id": project_id,
        "user_id": user_id
      })

      if assignment is not None:
        return jsonify({"message": "Developer already assigned."}), 400

      # Assign the developer to the project
      session.execute(
        insert(Project_Assignment_Table).values(
            project_id = project_id,
            user_id = user_id
        )
      )

      # Increase the number of people by 1
      project = session.get(Project_Table, project_id)
      session.execute(
        update(Project_Table)
        .where(Project_Table.project_id == project_id)
        .values(number_of_people=(project.number_of_people+1))
      )

      session.execute(
        update(Metric_Assignment_Table)
        .where(Metric_Assignment_Table.project_id == project_id)
        .where(Metric_Assignment_Table.metric_id == 2)
        .values(metric_value=(project.number_of_people+1))
      )
      session.commit()
      team_members = session.scalars(
            select(User_Table)
            .join(Project_Assignment_Table, User_Table.user_id == Project_Assignment_Table.user_id)
            .filter(Project_Assignment_Table.project_id == project.project_id)
            .order_by(User_Table.user_id)
        ).all()

      response = {
        "message": 'Developer assigned successfully.', 
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
      response = {"message": 'Developer could not be assigned.'}
      code = 500

    return jsonify(response), code
