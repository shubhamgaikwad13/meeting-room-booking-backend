from flask import Blueprint, request
import json
from ..db import connect_db
from ..models.Employee import Employee

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/', methods=['GET'])
def get_employees():
    db = connect_db()
    cursor = db.cursor()

    query = '''SELECT * FROM Employee'''

    try:
        cursor.execute(query)
        employees = cursor.fetchall() 
        return Employee.get_employees(employees)
    except:
        print('Failed to select records')
        return "404"
    


@employee_bp.route('/<id>', methods=['GET'])
def get_employee():
    pass


@employee_bp.route('/', methods=['POST'])
def add_employee():
    db = connect_db()
    cursor = db.cursor()

    query = '''INSERT INTO Employee(_id, first_name, last_name, email, password, phone, designation, is_admin) 
                VALUES (%(_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(designation)s, %(is_admin)s)'''
   
    params = dict(**request.args)
    
    try:
        cursor.execute(query, params)
        db.commit()
        return "202"
    except:
        print('Failed to insert record')
        return "404"



@employee_bp.route('/', methods=['PUT'])

def update_employee():
    pass


@employee_bp.route('/<id>', methods=['DELETE'])
def delete_employee():
    pass
