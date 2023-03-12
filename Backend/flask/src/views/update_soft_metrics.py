from sqlalchemy import create_engine, select, update
from flask import request, jsonify
from . import views
from app import session, token_required
from flask_cors import cross_origin # type: ignore
from sqlalchemy.exc import SQLAlchemyError
from database import *
from datetime import datetime


@views.route('/update_soft_metrics', methods=['POST'])
@cross_origin()
@token_required
def update_soft_metrics(auth_user):
    data = request.json

    server_token = data.get('server_token')
    project_id = data.get('project_id')
    updated_metrics = data.get('updated_metrics')

    try:
        # retrieve the metric assignments for the project
        metric_assignments = session.query(Metric_Assignment_Table).filter_by(project_id=int(project_id)).all()

        # update the values of the metrics in the metric assignments
        for metric in updated_metrics:
            for data_metric in metric_assignments:
                if metric['metric_id'] == data_metric.metric_id:
                    data_metric.metric_value = metric['value']
                   
        # commit the changes to the database
        session.commit()

        project = session.get(Project_Table, project_id)

        start = project.project_start
        end = project.project_end

        # Percentage of the way through the project
        time_elapsed = min((datetime.now()-start)/(end-start)*100, 100)
        for data_metric in metric_assignments:
            if data_metric.metric_id == 13:
                actual_cost = data_metric.metric_value
            if data_metric.metric_id == 14:
                work_completed = data_metric.metric_value/100
            if data_metric.metric_id == 16:
                total_budget = data_metric.metric_value
        
        planned_value = time_elapsed * total_budget
        earned_value = work_completed * total_budget

        # Calculate SPI
        if planned_value == 0:
            spi = 1
        else:
            spi = earned_value / planned_value

        session.execute(
            update(Metric_Assignment_Table)
            .where(Metric_Assignment_Table.project_id == project_id)
            .where(Metric_Assignment_Table.metric_id == 4)
            .values(metric_value=spi)
        )

        # Calulate CPI
        if actual_cost == 0:
            cpi = 1
        else:
            cpi = earned_value / actual_cost

        session.execute(
            update(Metric_Assignment_Table)
            .where(Metric_Assignment_Table.project_id == project_id)
            .where(Metric_Assignment_Table.metric_id == 5)
            .values(metric_value=cpi)
        )

        session.commit()

        # retrieve the updated metric assignments
        updated_metric_assignments = session.query(Metric_Assignment_Table, Metric_Table)\
            .join(Metric_Table, Metric_Assignment_Table.metric_id == Metric_Table.metric_id)\
            .filter(Metric_Assignment_Table.project_id == int(project_id))\
            .order_by(Metric_Assignment_Table.metric_id).all()

        # session.query(Metric_Assignment_Table).filter_by(project_id=int(project_id)).all()
        updated_metrics = [{
            "metric_description" : metric.Metric_Table.metric_desc,
            "metric_id" : metric.Metric_Table.metric_id,
            "metric_type" : metric.Metric_Table.metric_type,
            "value" : metric.Metric_Assignment_Table.metric_value
        } for metric in updated_metric_assignments]
            
        return jsonify(updated_metrics), 200

    except SQLAlchemyError as e:
        # handle the exception
        session.rollback()
        return jsonify('Unable to update the soft metrics'), 500
    finally:
        # close the database connection
        session.close()
