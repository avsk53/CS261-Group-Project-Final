from functools import wraps
from os import environ
from flask import Flask, request, jsonify
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS # type: ignore
import jwt

app = Flask(__name__)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = 'D\xb4KZ\xd8\xda\xb0\x9e\xd3\xc9*\xe2\xe5>\x1d\x94qE\xc3\xc3jx\x1d\xd6'
cfg = app.config

db = create_engine(environ.get("DATABASE_URL"))

Session = sessionmaker(db)
session = Session()

from database import *
from objects import *
from views import *

app.register_blueprint(views)

'''
As this is a prototype of our system, we are using app.run() to run a development server.
We are aware that this would not be suitable if the system were to be deployed for real,
if this were the case we would use the production WSGI server Gunicorn.
'''

if __name__ == "__main__":
  app.run(host="0.0.0.0",port=5555)


def token_required(f):
  @wraps(f)
  def decorator(*args, **kwargs):
    token = None

    if 'x-access-token' in request.headers:
      token = request.headers['x-access-token']
    
    if not token:
      return jsonify({'message': 'a valid token is missing'})

    try:
      data = jwt.decode(token, app.config['SECRET_KEY'])
      current_user = session.scalar(select(User_Table).filter_by(user_id=data['public_id']).limit(1))
    except:
      return jsonify({'message': 'token is invalid'})
    return f(current_user, *args, **kwargs)
  return decorator