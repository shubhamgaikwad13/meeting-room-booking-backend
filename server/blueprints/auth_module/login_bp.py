# imports 
from flask import Blueprint, request, jsonify, session
from ...db import connect_db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from functools import wraps
import os


from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps

# secret key from .env
# SECRET_KEY = os.environ.get("JWT_KEY")

# def verify_token():
#     @wraps(f)
#     def decorated(*args, **kwargs):
#         token = None
#         # jwt is passed in the request header
#         if 'x-access-token' in request.headers:
#             token = request.headers['x-access-token']
#         # return 401 if token is not passed
#         if not token:
#             return jsonify({'message' : 'Token is missing !!'}), 401



# route for login
login_bp = Blueprint('auth', __name__, url_prefix='/auth')



# route for generating token
@login_bp.route('/', methods=['POST', 'GET'])
def login():
    user_credentials = request.get_json()
    db = connect_db()
    cursor = db.cursor()
    
    if not user_credentials or not user_credentials['email'] or not user_credentials['password']:
        return {"status": 404, "message": "Login credentials required"}

    is_user_query = "SELECT email, password FROM Employee WHERE email=%(email)s"

    cursor.execute(is_user_query, user_credentials)
    # print("config", app.config)

    user = cursor.fetchone()
    # print("user: ", user_credentials['password'])
    if not user:
        return {'status': 400, 'message': "User not found."}

    if check_password_hash(user[1],user_credentials['password']):
        token = create_access_token(identity = user_credentials["email"])
  
        return {'token' : token}
    else:
        return jsonify({"message" : "credentials are wrong"})