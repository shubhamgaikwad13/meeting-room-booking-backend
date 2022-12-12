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
    # print(request.form['id'])
    # print(request.args.get('id') )
    db = connect_db()
    cursor = db.cursor()
    query = "INSERT INTO Employee VALUES(3, 'shree', 'raj', 'sggs@mail.com','Opcito123', '5235235', 'trainee', true, false, null,null,null,null)"
    try:
        cursor.execute(query)
    except:
        print('some err')
    db.commit()
    return 202


@employee_bp.route('/', methods=['PUT'])
def update_employee():
    pass


@employee_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee():
    pass
