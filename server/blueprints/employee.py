from flask import Blueprint, jsonify, request
from ..db import connect_db
from ..models import Employee

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/', methods=['GET'])
def get_employees():
    output = {'msg': 'hi employee'}
    return jsonify(output)


@employee_bp.route('/', methods=['GET'])
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
    except:
        print('Failed to insert record')
    db.commit()
    return "202"


@employee_bp.route('/', methods=['PUT'])
def update_employee():
    pass


@employee_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee():
    pass
