from flask import Blueprint, request, g, jsonify
from ...db import connect_db
from .models import Teams
from server.blueprints.teams_module.constant import *
from http import HTTPStatus

# Creates Bluprint at team_bp with url
team_bp = Blueprint('team', __name__, url_prefix='/team')

# Each time the url is called, before_request runs
@team_bp.before_request
def before_request():
    g.db = connect_db()

# 0. Add TeamMember
# 1. Create Team
# 2. Get Teams List
# 3. Update Team
# 4. Get Team Members 
# 5. Get Team by name

# 0. Adds team member to the team
@team_bp.route('/addteammember', methods=['POST'])
def add_team_member():
    cursor = g.db.cursor()
    query = '''INSERT INTO TeamMember (team_id,employee_id) values(1,3);'''


# 1. Creates the teams in database
@team_bp.route('/createteam', methods=['POST'])
def create_team():
    cursor = g.db.cursor()
    query = '''INSERT INTO''' 

# 2. Gets list of teams and its members
@team_bp.route('/', methods=['GET'])
def get_teams():
    cursor = g.db.cursor()
    #Return Team name and TeamMembers count through an inner join of Team and TeamMembers tables
    query = '''SELECT Team.name, count(TeamMember.employee_id) FROM TeamMember INNER JOIN Team ON TeamMember.team_id=Team._id group by team_id order by name;'''
    try:
        cursor.execute(query)
        teams = cursor.fetchall()
        teamsList = Teams.get_teams(teams)
        statusCode = HTTPStatus.OK

        return jsonify({"TeamsList" : teamsList}), statusCode

    except Exception:
        statusCode = HTTPStatus.BAD_REQUEST
        return jsonify({"message": TEAMS_NOT_FOUND}), statusCode



# 5. Gets team of particular name and its members
@team_bp.route('/<name>', methods=['GET'])
def get_team_by_name(name):
    db = connect_db()
    cursor = db.cursor()

    query = '''SELECT Team.name, count(TeamMember.employee_id) FROM TeamMember INNER JOIN Team ON TeamMember.team_id=Team._id WHERE name=%(name)s;'''
    params = {'name': name}

    try:
        cursor.execute(query, params)
        team = cursor.fetchone()
        Team = Teams.get_team(team)
        statusCode = HTTPStatus.OK
        if Team:
            statusCode = HTTPStatus.OK
            return jsonify(Team), statusCode
        statusCode = HTTPStatus.BAD_REQUEST
        error = TEAM_NOT_FOUND.format(teamName = name)
        return jsonify({"Error": error}), statusCode
        
    except Exception as e:
        statusCode = HTTPStatus.BAD_REQUEST
        return jsonify({"Error": e}), statusCode

