from flask import Blueprint, request,g, jsonify
from ...db import connect_db
# from ...models.Employee import Employee
from .models import Employee

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

@employee_bp.before_request
def before_request():
    g.db = connect_db()


@employee_bp.route('/', methods=['GET'])
def get_employees():
    cursor = g.db.cursor()

    query = '''SELECT * FROM Employee WHERE is_active=true'''

    try:
        cursor.execute(query)
        employees = cursor.fetchall() 
        return Employee.get_employees(employees)
    except:
        print('Failed to select records')
        return "404"
    

@employee_bp.route('/<id>', methods=['GET'])
def get_employee_by_id(id):
    db = connect_db()
    cursor = db.cursor()

    query = '''SELECT * FROM Employee WHERE _id = %(_id)s'''
    params = {'_id': id}

    try:
        cursor.execute(query, params)
        employee = cursor.fetchone() 
        print(employee)
        return Employee.get_employee(employee)
    except Exception as e:
        print(e)
        return "404"
    

@employee_bp.route('/', methods=['POST'])
def add_employee():
    db = connect_db()
    cursor = db.cursor()

    query = '''INSERT INTO Employee(_id, first_name, last_name, email, password, phone, designation, is_admin) 
                VALUES (%(_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(designation)s, %(is_admin)s);'''

    
    try:
        cursor.execute(query, request.get_json())
        db.commit()
        return "201"
    except Exception as e:
        print('Failed to insert record')
        return {"error" : str(e)}


@employee_bp.route('/<id>', methods=['DELETE'])
def delete_employee_by_id(id):
    db = connect_db()
    cursor = db.cursor()

    query = '''UPDATE Employee SET is_active = false WHERE _id = %(_id)s'''
    params = {'_id': id}

    try:
        cursor.execute(query, params)
        db.commit()
        return "202"
    except Exception as e:
        print(e)
        return "404"


@employee_bp.route('/<id>', methods=['PATCH'])
def update_employee(id):
    db = connect_db()
    cursor = db.cursor()

    query = '''UPDATE Employee SET '''
    
    for field in request.get_json().keys():
        query = query + f'{field}=%({field})s,'
 
    query = query[:-1] + f'WHERE _id={id}'

    try:
        cursor.execute(query, request.get_json())
        db.commit()
        return "202"
    except Exception as e:
        print(e)
        return "404"
