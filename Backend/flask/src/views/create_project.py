from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from . import get_projects
from app import session, token_required
from sqlalchemy import select, insert, update
from database import *
from datetime import datetime
from evaluation_improvements import *
from github_scraping import *

@views.route("/create_project", methods=["POST"])
@cross_origin()
@token_required
def create_project(auth_user):
  if auth_user.user_role == 0 or auth_user.user_role == 3:
    return jsonify({'message': 'You are not authorized to access this endpoint'}), 401
  
  if request.method == "POST":
    
    data = request.json

    token = data["server_token"]
    project_manager_id = data["user_id"]

    form_data = data["form_data"]
    project_name = form_data["project_name"]
    project_start = form_data["project_start_date"]
    project_end = form_data["project_end_date"]
    github_link = form_data["github_url"]
    soft_metrics = form_data["soft_metrics"]

    # try:
    if True:
      for m in soft_metrics:
        if int(m["metric_id"]) == 2:
          teamSize = float(m['metric_value'])
          break

      # Insert project into database
      project_id = session.execute(
        insert(Project_Table).values(
          project_name = project_name,
          project_start = project_start,
          project_end = project_end,
          github_link = github_link,
          number_of_people = teamSize,
          project_manager_id = project_manager_id
        )
      ).inserted_primary_key[0]

      start = datetime.strptime(project_start, '%Y-%m-%d')
      end = datetime.strptime(project_end, '%Y-%m-%d')

      # Percentage of the way through the project
      time_elapsed = min((datetime.now()-start).total_seconds()/(end-start).total_seconds(), 1)

      actual_cost = 0
      work_completed = 0
      total_budget = 0
      for m in soft_metrics:
        if int(m["metric_id"]) == 12:
          actual_cost = float(m['metric_value'])
        if int(m["metric_id"]) == 13:
          work_completed = float(m['metric_value'])/100
        if int(m["metric_id"]) == 15:
          total_budget = float(m['metric_value'])

      planned_value = time_elapsed * total_budget
      earned_value = work_completed * total_budget

      # Calculate SPI
      if planned_value == 0:
          spi = 0
      else:
          spi = earned_value / planned_value

      # Calulate CPI
      if actual_cost == 0:
          cpi = 0
      else:
          cpi = earned_value / actual_cost

      soft_metrics.append({
        "metric_id": 4,
        "metric_value": spi
      })

      soft_metrics.append({
        "metric_id": 5,
        "metric_value": cpi
      })

      # Insert all provided soft metrics
      set_metrics = []
      for m in soft_metrics:
        set_metrics.append(int(m["metric_id"]))
        session.execute(
          insert(Metric_Assignment_Table).values(
            metric_id = m["metric_id"],
            project_id = project_id,
            metric_value = m["metric_value"]
          )
        )

      # Ensure all other metrics get inserted
      # Work done (%) gets inserted as 0 here
      number_of_metrics = 16
      for i in range(number_of_metrics):
        if i not in set_metrics:
          session.execute(
            insert(Metric_Assignment_Table).values(
              metric_id = i,
              project_id = project_id,
              metric_value = 1 if i == 2 else 0
            )
          )
      session.commit()

      # TODO: When GitHub scraping is implemented:
      scrape(project_id)

      evaluation(project_id, 0)  

      # Generate initial evaluation

      project = session.get(Project_Table, project_id)
      recent = session.scalars(
          select(Project_Evaluation_Table)
          .filter_by(project_id=project.project_id)
          .order_by(Project_Evaluation_Table.evaluation_date.desc())
      ).first()

      session.execute(
          update(Metric_Assignment_Table)
          .where(Metric_Assignment_Table.project_id == project_id)
          .where(Metric_Assignment_Table.metric_id == 2)
          .values(metric_value=0)
      )

      session.execute(
          update(Project_Table)
          .where(Project_Table.project_id == project_id)
          .values(number_of_people=0)
      )
      session.commit()

      return jsonify({
        "project_id": project_id,
        "project_name": project.project_name,
        "recent_evaluation_label": recent.evaluation_label,
        "project_manager_name": auth_user.username
      }), 200
    # except:
    #   # If anything goes wrong return a generic error message
    #   return jsonify({"message": "Could not create project."}), 500


