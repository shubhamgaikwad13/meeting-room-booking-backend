from flask import Blueprint, request, g
from ...db import connect_db
from .models import Teams
from . import constants
import json

# Creates Bluprint at team_bp with url
team_bp = Blueprint('team', __name__, url_prefix='/team')

# Each time the url is called, before_request runs
@team_bp.before_request
def before_request():
    g.db = connect_db()

# Get method to get list of teams and its members
@team_bp.route('/', methods=['GET'])
def get_teams():
    cursor = g.db.cursor()
    #Return Team name and TeamMembers count through an inner join of Team and TeamMembers tables
    query = '''SELECT Team.name, count(TeamMember.employee_id) FROM TeamMember INNER JOIN Team ON TeamMember.team_id=Team._id group by team_id;'''

    try:
        cursor.execute(query)
        teams = cursor.fetchall()
        return Teams.get_teams(teams)
    except:
        print('Failed to select records')
        return json.dumps({"error_code": 404, "message": constants.GetTeamsError})

# Get method to get team of particular name and its members
@team_bp.route('/<name>', methods=['GET'])
def get_team_by_name(name):
    db = connect_db()
    cursor = db.cursor()

    query = '''SELECT Team.name, count(TeamMember.employee_id) FROM TeamMember INNER JOIN Team ON TeamMember.team_id=Team._id group by team_id;'''
    # query = '''SELECT * FROM Team WHERE name = %(name)s'''
    params = {'name': name}

    try:
        cursor.execute(query, params)
        team = cursor.fetchone()
        print(team)
        return Teams.get_teams(team)
    except Exception as e:
        print(e)
        return "404"


# @employee_bp.route('/', methods=['POST'])
# def add_employee():
#     db = connect_db()
#     cursor = db.cursor()

#     query = '''INSERT INTO Employee(_id, first_name, last_name, email, password, phone, designation, is_admin) 
#                 VALUES (%(_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(designation)s, %(is_admin)s)'''

#     try:
#         cursor.execute(query, request.get_json())
#         db.commit()
#         return "200"
#     except:
#         print('Failed to insert record')
#         return "404"


# @employee_bp.route('/<id>', methods=['DELETE'])
# def delete_employee_by_id(id):
#     db = connect_db()
#     cursor = db.cursor()

#     query = '''UPDATE Employee SET is_active = false WHERE _id = %(_id)s'''
#     params = {'_id': id}

#     try:
#         cursor.execute(query, params)
#         db.commit()
#         return "202"
#     except Exception as e:
#         print(e)
#         return "404"


# @employee_bp.route('/<id>', methods=['PATCH'])
# def update_employee(id):
#     db = connect_db()
#     cursor = db.cursor()

#     query = '''UPDATE Employee SET '''

#     for field in request.get_json().keys():
#         query = query + f'{field}=%({field})s,'

#     query = query[:-1] + f'WHERE _id={id}'

#     try:
#         cursor.execute(query, request.get_json())
#         db.commit()
#         return "202"
#     except Exception as e:
#         print(e)
#         return "404"
