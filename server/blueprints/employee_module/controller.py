from flask import Blueprint, request, g, jsonify
from http import HTTPStatus
from ...db import connect_db
from .EmployeeDAO import Employee
from .service import EmployeeValidation
from .constant import *
from mysql.connector import errorcode
from mysql.connector import Error as MySQLError
from ...utils import make_response

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


# connects to db before request if not connected already
@employee_bp.before_request
def before_request():
    g.db = connect_db()


# closes db connection after each request
@employee_bp.after_request
def after_request(response):
    g.db.close()
    return response


# api for fetching all employees
@employee_bp.route('/', methods=['GET'])
def get_employees():
    try:
        employees = Employee.get_employees()  # fetches employees in list
        if employees:
            return make_response(employees, key="employees"), HTTPStatus.OK

        return make_response(NO_EMPLOYEES_FOUND), HTTPStatus.OK
    except Exception as e:
        return make_response(FETCH_EMPLOYEED_FAILED, key="error"), HTTPStatus.BAD_REQUEST


# api for fetching employee by id
@employee_bp.route('/<id>', methods=['GET'])
def get_employee_by_id(id):
    try:
        employee = Employee.get_employee_by_id(
            id)  # fetches employee in object

        if employee is None:
            return make_response(EMPLOYEE_NOT_FOUND), HTTPStatus.OK

        return make_response(data=employee.__dict__, key='employee'), HTTPStatus.OK

    except Exception as e:
        return make_response(data=str(e), key="error"), HTTPStatus.BAD_REQUEST


# api for adding an employee to the database
@employee_bp.route('/', methods=['POST'])
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
