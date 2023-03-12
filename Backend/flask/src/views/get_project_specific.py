import sys
from flask import request, jsonify
from . import views
from app import session, token_required
from database import *
from flask_cors import cross_origin # type: ignore
from sqlalchemy import select
from datetime import datetime
from evaluation_improvements import *
from github_scraping import *

@views.route('/get_project_specific', methods=['POST'])
@cross_origin()
@token_required
def get_project_specific(auth_user):
    
    data = request.form
    
    token = data.get("server_token")
    project_id = data.get("project_id")

    # Fetch the project and check if it exists
    project = session.get(Project_Table, project_id)

    if project is not None:
        # Get more detailed information about project
        manager = session.get(User_Table, project.project_manager_id)
        
        recent = session.scalars(
            select(Project_Evaluation_Table)
            .filter_by(project_id=project.project_id)
            .order_by(Project_Evaluation_Table.evaluation_date.desc())
        ).first()

        # Generate a new evaluation if it's been a week since the last automatic evaluation
        today = datetime.now()
        diff1 = (today - manager.last_logged_in).days
        diff2 = (today - recent.evaluation_date).days
        if diff1 >= 7 and diff2 >= 1:
            scrape(project_id)
            evaluation(int(project_id), 0)

        # Get evaluation history
        evaluations = session.scalars(
            select(Project_Evaluation_Table)
            .filter_by(project_id=project.project_id)
            .order_by(Project_Evaluation_Table.evaluation_date.desc())
        ).all()
        recent = evaluations[0]

        metrics = session.scalars(
            select(Metric_Table)
            .order_by(Metric_Table.metric_id)
        ).all()

        metric_assignments = session.scalars(
            select(Metric_Assignment_Table)
            .filter_by(project_id=project.project_id)
            .order_by(Metric_Assignment_Table.metric_id)
        ).all()

        current_values = {}
        for m in metric_assignments:
            current_values[m.metric_id] = m.metric_value
        
        improvement_metrics = session.scalars(
            select(Improvement_Metrics_Table)
            .filter_by(evaluation_id=recent.evaluation_id)
            .order_by(Improvement_Metrics_Table.metric_id)
        ).all()

        for x,i in enumerate(improvement_metrics):
            if current_values.get(i.metric_id) is None:
                improvement_metrics[x] = (i.improvement_value, i)
            else:
                improvement_metrics[x] = (abs(i.improvement_value - current_values[i.metric_id]), i)
        improvement_metrics.sort(key=lambda x: x[0], reverse=True)
        improvement_metrics = [i[1] for i in improvement_metrics]

        team_members = session.scalars(
            select(User_Table)
            .join(Project_Assignment_Table, User_Table.user_id == Project_Assignment_Table.user_id)
            .filter(Project_Assignment_Table.project_id == project.project_id)
            .order_by(User_Table.user_id)
        ).all()
    
        
		# Format the fetched data in the correct endpoint format
        out = {
                "project_id": project.project_id, 
                "project_name": project.project_name, 
                "github_url": project.github_link, 
                "project_manager_name": manager.username, 
                "project_start_date": project.project_start, 
                "project_end_date": project.project_end, 
                "number_of_people": project.number_of_people,
                "recent_evaluation": {
                    "evaluation_type": recent.evaluation_type,
                    "evaluation_label": recent.evaluation_label,
                    "evaluation_date": recent.evaluation_date,
                    "improvement_metrics": [
                        {
                            "metric_id": m.metric_id, 
                            "metric_description": metrics[m.metric_id].metric_desc, 
                            "_rowVariant": "success" if (m.improvement_value > metric_assignments[m.metric_id].metric_value) else "info" if (m.improvement_value == metric_assignments[m.metric_id].metric_value) else "danger",
                            "value": m.improvement_value,
                            "diff": abs(m.improvement_value - current_values.get(m.metric_id, 0)),
                            "current_value": current_values.get(m.metric_id, 0),
                            "display_arrow": metrics[m.metric_id].metric_type
                        } for m in improvement_metrics
                    ]
                },
                "evaluation_history": [
                    {
                        "evaluation_type": e.evaluation_type,
                        "evaluation_label": e.evaluation_label,
                        "evaluation_date": e.evaluation_date
                    } for e in evaluations
                ], 
                "current_metrics": [
                    {
                        "metric_id": m.metric_id, 
                        "metric_description": m.metric_desc, 
                        "metric_type": m.metric_type,
						"value": current_values.get(x, 0), 
					} for x,m in enumerate(metrics)
				], 
                "team_members": [
					{
						"username": t.username,
                        "user_id": t.user_id,
                        "email": t.email,
                        "role": t.role_desc
					} for t in team_members
				]
			}
        return jsonify(out), 200
    else:
        return jsonify({'message': 'Project not found'}), 404