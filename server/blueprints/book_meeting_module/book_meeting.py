# imports 
from flask import Blueprint, request, g
from ...db import connect_db
from .models import Meeting, MeetingMember

# setting up blueprint meeting api 
meeting_bp = Blueprint('meetings', __name__, url_prefix='/meetings')

# before request for meeting api 
@meeting_bp.before_request
def before_request():
    g.db = connect_db()
    
# CRUD for meeting api 
@meeting_bp.route('/', methods = ['GET'])
def get_meetings():
    cursor = g.db.cursor()
    query = '''SELECT * FROM Meeting'''
    try:
        cursor.execute(query)
        meetings = cursor.fetchall()
        return Meeting.get_meetings(meetings)
    except:
        print('Failed to fetch meeting')
        return "401"
    
