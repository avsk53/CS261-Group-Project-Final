from flask import request, jsonify
from . import views
from app import session, token_required
from database import *
from flask_cors import cross_origin # type: ignore
from sqlalchemy import update
from evaluation_improvements import evaluation
from github_scraping import *

# Evaluation handler function
@views.route('/request_evaluation', methods=['POST'])
@cross_origin()
@token_required
def request_evaluation(auth_user):
    # Parse request data
    data = request.json

    token = data.get('server_token')
    project_id = data.get('project_id')

    try:
        evaluation(int(project_id), 1)
        scrape(project_id)
        return jsonify({'message': 'Project evaluation successful.'}), 200
    except:
        return jsonify({'message': 'Project evaluation failed.'}), 500
