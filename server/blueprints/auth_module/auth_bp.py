# imports 
from flask import Blueprint, request, jsonify, session
from ...db import connect_db
import jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
from ...settings import SECRET_KEY
from ...models.Employee import Employee

# decorator for verifying the JWT
def token_required():
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        # return 401 if token is not passed
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401
        
        try:
            # decoding the payload to fetch the stored details
            data = jwt.decode(token, SECRET_KEY)
            print("data: ", data)
            current_user_query = '''SELECT * FROM email, password FROM Employee WHERE _id=%(id)s'''
            db = connect_db()
            cursor = db.cursor()
            cursor.execute(current_user_query, data)
            current_user = cursor.fetchone()
        except:
            return jsonify({
                'message' : 'Token is invalid !!'
            }), 401
        # returns the current logged in users contex to the routes
        return  f(current_user, *args, **kwargs)
  
    return decorated


# route function for login 
login_bp = Blueprint('login', __name__, url_prefix='/auth')

@login_bp.route('/', methods=['POST'])
def login():
    user_credentials = request.get_json()
    db = connect_db()
    cursor = db.cursor()
    
    if not user_credentials or not user_credentials['email'] or not user_credentials['password']:
        return {status: 404, message: "Login credentials required"}

    is_user_query = "SELECT email, password FROM Employee WHERE email=%(email)s"

    cursor.execute(is_user_query, user_credentials)
    # print("config", app.config)

    user = cursor.fetchone()
    # print("user: ", user)
    if not user:
        return {'status': 400, 'message': "User not found."}

    if check_password_hash(user[1] , user_credentials['password']):
        token = jwt.encode({
            'public_id': user[0],
            'exp' : datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY)
  
        return {'token' : token.decode('UTF-8')}

    # print("request: ",request.get_data())
    return "ok"
    
            