# imports 
from flask import Blueprint, request, jsonify
from ...db import connect_db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, set_access_cookies, unset_jwt_cookies
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from .constant import *
from http import HTTPStatus
from datetime import datetime, timedelta, timezone

# route for login
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


# route for generating token
@auth_bp.route('/', methods=['POST', 'GET'])
def login():
    try:
        user_credentials = request.get_json()
        # print("cred ", user_credentials)
        db = connect_db()
        cursor = db.cursor()
        
        if not user_credentials or not user_credentials['email'] or not user_credentials['password']:
            raise Exception(MISSING_CREDENTIALS)
        # cheking type for login credentials
        if type(user_credentials["email"]) is not str or type(user_credentials["password"]) is not str:
            raise Exception(STRING_REQUIRED)

        is_user_query = "SELECT email, password FROM Employee WHERE email=%(email)s"

        cursor.execute(is_user_query, user_credentials)
        # print("config", app.config)

        user = cursor.fetchone()
        # print("user: ", user_credentials['password'])
        if not user:
            raise Exception(INVALID_USER)

        # checking hashed password
        if check_password_hash(user[1],user_credentials['password']):
            response = jsonify({"message": "Login successful."})
            now = datetime.now(timezone.utc)
            # print("created: ", now)
            access_token = create_access_token(identity = user_credentials["email"])
            set_access_cookies(response, access_token)
            return response
        else:
            raise Exception(WRONG_PASSWORD)
    
    # exception for missing any key
    except KeyError as missing:
        return {"error" : {"message" : FAILED_VALIDATION, "parameter" : str(missing)}}, HTTPStatus.BAD_REQUEST

    except Exception as e:
        return jsonify({"error" : str(e)}), HTTPStatus.BAD_REQUEST


# route for logout
@auth_bp.route("/logout", methods=["POST"])
def logout():
    response = jsonify({"message": "logout successful"})
    unset_jwt_cookies(response)
    return response

# demo route for jwt authentication
@auth_bp.route("/protected")
@jwt_required()
def protected():
    return jsonify(foo="bar")
