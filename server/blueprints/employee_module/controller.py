from flask import Blueprint, request, g, jsonify
from http import HTTPStatus
from ...db import connect_db
from .EmployeeDAO import Employee
from .service import EmployeeValidation
from flask_jwt_extended import jwt_required, get_jwt_identity
from .constant import *
from mysql.connector import errorcode
from mysql.connector import Error as MySQLError
from ...utils import make_response

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


# api for fetching all employees
@employee_bp.route('/', methods=['GET'])
@jwt_required()
def get_employees():
    try:
        employees = Employee.get_employees()  # fetches employees in list
        if employees:
            return make_response(employees, key="employees"), HTTPStatus.OK

        return make_response(NO_EMPLOYEES_FOUND), HTTPStatus.OK
    except Exception as e:
        return make_response(FETCH_EMPLOYEES_FAILED, key="error"), HTTPStatus.BAD_REQUEST


# api for fetching employee by id
@employee_bp.route('/<id>', methods=['GET'])
@jwt_required()
def get_employee_by_id(id):
    try:
        employee = Employee.get_employee_by_id(
            id)  # fetches employee in object

        if employee is None:
            return make_response(EMPLOYEE_NOT_FOUND), HTTPStatus.NOT_FOUND

        return make_response(data=employee.__dict__, key='employee'), HTTPStatus.OK

    except Exception as e:
        return make_response(data=str(e), key="error"), HTTPStatus.BAD_REQUEST


# api for adding an employee to the database
@employee_bp.route('/', methods=['POST'])
@jwt_required()
def add_employee():
    params = request.get_json()

    try:
        # validates request parameters and throws exception for invalid params
        EmployeeValidation.validate(params)

        # checks if request is being made by admin
        if not Employee.is_admin(params['created_by']):
            raise Exception(ONLY_ADMIN_ADDS_USER)

        employee = Employee(**params)
        employee.save()  # inserts employee record in the database

    except MySQLError as err:
        # Error handling for duplicate entries for phone, email and id
        if err.errno == errorcode.ER_DUP_ENTRY:
            for key in DUP_ENTRY:
                if key in err.msg:
                    return make_response(dup_message(key), 'error'), HTTPStatus.BAD_REQUEST

        # Other mysql errors
        return make_response(str(err), 'error'), HTTPStatus.BAD_REQUEST

    except Exception as e:
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    return make_response(EMPLOYEE_ADDED), HTTPStatus.OK


# api for deleting an employee by id
@employee_bp.route('/<id>', methods=['DELETE'])
@jwt_required()
def delete_employee_by_id(id):
    try:
        params = request.get_json()

        # checks if request is being made by admin
        if not Employee.is_admin(params['updated_by']):
            raise Exception("Only admin can delete the user.")

        # if employee exists then deletes otherwise shows error
        employee = Employee.get_employee_by_id(id)

        if employee is None:
            return make_response(EMPLOYEE_NOT_FOUND), HTTPStatus.BAD_REQUEST

        employee.delete()  # if employee exists then soft deletes its record

    except Exception as e:
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    return make_response(EMPLOYEE_DELETED), HTTPStatus.OK


# api for updating employee data - phone, designation, password
@employee_bp.route('/<id>', methods=['PATCH'])
@jwt_required()
def update_employee(id):
    params = request.get_json()

    try:
        EmployeeValidation.validate_update_request(params)

        # checks if request is being made by admin
        if not Employee.is_admin(params['updated_by']):
            raise Exception(ONLY_ADMIN_ADDS_USER)
        
        # if employee exists then updates otherwise shows error
        employee = Employee.get_employee_by_id(id)
        if employee is None:
            return make_response(EMPLOYEE_NOT_FOUND), HTTPStatus.BAD_REQUEST

        employee.update(params)
        return make_response("Employee record updated successfully."), HTTPStatus.OK

    except Exception as e:
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST
    


# internal api for fake inserts of employee records
@employee_bp.route('/fake', methods=['GET'])
def fake_inserts():
    cursor = g.db.cursor()

    query = '''INSERT INTO Employee(_id, first_name, last_name, email, password, phone, designation)
                    VALUES (%(_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(designation)s)'''

    id = 3000
    phone = 9000000000

    for i in range(3000, 10000):
        params = {
            "_id": i,
            "first_name": "John",
            "last_name": "Doe",
            "email": f"johndoe{i}@mail.com",
            "password": "Opcito@123",
            "phone": phone + i,
            "designation": "HR"
        }

        cursor.execute(query, params)
        g.db.commit()

    return "fake records inserted"


# User details after verifying token
@employee_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    try:
        user_email = get_jwt_identity()

        employee = Employee.get_employee_by_email(str(user_email))

        if employee is not None:
            return employee
        else:
            raise Exception("Employee Not Found.")

    except Exception as e:
        return({"message" : str(e)})


# fake api to test profile img
@employee_bp.route('/img', methods=['GET'])
def show_base64_img():
    return f"<img  height='100' src='data:image/webp;base64,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'/>"