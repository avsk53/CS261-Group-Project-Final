from flask import request, jsonify
from flask_cors import cross_origin # type: ignore
from . import views
from app import session, token_required
from sqlalchemy import insert, update, select, or_
from database import *

@views.route("/search_user", methods=["POST"])
@cross_origin()
@token_required
def search_user(auth_user):
  if request.method == "POST":
    data = request.get_json()

    token = data["server_token"]
    substring = data.get("substring")

    # These are optional - provide them for pagination
    page_size = data.get("page_size")
    page = data.get("page")

    # Get all users whose names or emails match the substring
    filters = [
      User_Table.username.contains(substring),
      User_Table.email.contains(substring)
    ]

    users = session.scalars(
      select(User_Table)
      .filter(or_(*filters))
    ).all()


    # Format the response
    response = [
      {
        "username": user.username,
        "email": user.email,
        "user_id": user.user_id
      } for user in users
    ]

    # If the request wants a paginated response
    if page_size is not None and page is not None:
      if len(response) == 0:
        # Can't paginate an empty list
        response = {
          "total_pages": 0,
          "users": []
        }
      else:
        # Split the response into pages of the requested size
        paginated = []
        for i in range(0, len(response), page_size):
            paginated.append(response[i:i+page_size])

        # Return the requested page, with the total number of pages
        if page < 1 or page > len(paginated):
          return jsonify({"message": "Invalid page number."}), 400

        response = {
          "total_pages": len(paginated),
          "users": paginated[page-1]
        }
    else:
      response = {
        "total_pages": 1,
        "users": response
      }

    return jsonify(response), 200
