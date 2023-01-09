from flask import Blueprint, request, g, jsonify
from http import HTTPStatus
from ...db import connect_db
from .EmployeeDAO import Employee
from .service import EmployeeValidation
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended.exceptions import JWTDecodeError
from .constant import *
from mysql.connector import errorcode
from mysql.connector import Error as MySQLError
from ...utils import make_response
import logging

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')

logger = logging.getLogger('employee_module')

# api for fetching all employees
@employee_bp.route('/', methods=['GET'])
def get_employees():
    logger.info("Fetching all employees.")
    try:
        employees = Employee.get_employees()  # fetches employees in list
        if employees:
            logger.info("All employees fetched successfully.")
            return make_response(employees, key="employees"), HTTPStatus.OK

        logger.info(NO_EMPLOYEES_FOUND)
        return make_response(NO_EMPLOYEES_FOUND), HTTPStatus.OK
    except Exception as e:
        logger.error(str(e))
        return make_response(FETCH_EMPLOYEED_FAILED, key="error"), HTTPStatus.BAD_REQUEST


# api for fetching employee by id
@employee_bp.route('/<id>', methods=['GET'])
def get_employee_by_id(id):
    logger.info(f"Fetching employee with id {id}")
    try:
        employee = Employee.get_employee_by_id(
            id)  # fetches employee in object

        if employee is None:
            logger.info(EMPLOYEE_NOT_FOUND)
            return make_response(EMPLOYEE_NOT_FOUND), HTTPStatus.OK

        logger.info("Employee fetched successfully.")
        return make_response(data=employee.__dict__, key='employee'), HTTPStatus.OK

    except Exception as e:
        logger.error(str(e))
        return make_response(data=str(e), key="error"), HTTPStatus.BAD_REQUEST


# api for adding an employee to the database
@employee_bp.route('/', methods=['POST'])
def add_employee():
    params = request.get_json()
    logger.info("Adding a new employee.")
    try:
        # validates request parameters and throws exception for invalid params
        logger.info("Validating add request parameters.")
        EmployeeValidation.validate(params)

        # checks if request is being made by admin
        logger.info("Checking if only admin is adding an employee.")
        if not Employee.is_admin(params['created_by']):
            raise Exception(ONLY_ADMIN_ADDS_USER)

        employee = Employee(**params)
        logger.info("Inserting employee record in the database.")
        employee.save()  # inserts employee record in the database

    except MySQLError as err:
        logger.error(str(err))
        # Error handling for duplicate entries for phone, email and id
        if err.errno == errorcode.ER_DUP_ENTRY:
            for key in DUP_ENTRY:
                if key in err.msg:
                    return make_response(dup_message(key), 'error'), HTTPStatus.BAD_REQUEST

        # Other mysql errors
        return make_response(str(err), 'error'), HTTPStatus.BAD_REQUEST

    except Exception as e:
        logger.error(str(e))
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    logger.info(EMPLOYEE_ADDED)
    return make_response(EMPLOYEE_ADDED), HTTPStatus.OK


# api for deleting an employee by id
@employee_bp.route('/<id>', methods=['DELETE'])
def delete_employee_by_id(id):
    logger.info("Soft-Deleting an employee")
    try:
        params = request.get_json()

        # checks if request is being made by admin
        logger.info("Checking if only admin is deleting an employee.")
        if not Employee.is_admin(params['updated_by']):
            raise Exception("Only admin can delete the user.")

        # if employee exists then deletes otherwise shows error
        logger.info("Checking if employee exists in the database.")
        employee = Employee.get_employee_by_id(id)

        if employee is None:
            logger.info(EMPLOYEE_NOT_FOUND)
            return make_response(EMPLOYEE_NOT_FOUND), HTTPStatus.BAD_REQUEST
        
        logger.info("Soft-deleting employee record in the database.")
        employee.delete()  # if employee exists then soft deletes its record

    except Exception as e:
        logger.error(str(e))
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    logger.info("Employee deleted succesfully.")
    return make_response(EMPLOYEE_DELETED), HTTPStatus.OK


# api for updating employee data - phone, designation, password
@employee_bp.route('/<id>', methods=['PATCH'])
def update_employee(id):
    params = request.get_json()
    logger.info(f"Updating an employee {id}")

    try:
        EmployeeValidation.validate_update_request(params)

        # checks if request is being made by admin
        logger.info("Checking if only admin is updating an employee.")
        if not Employee.is_admin(params['updated_by']):
            raise Exception(ONLY_ADMIN_ADDS_USER)
        
        # if employee exists then updates otherwise shows error
        logger.info("Checking if employee exists in the database.")
        employee = Employee.get_employee_by_id(id)
        if employee is None:
            logger.info(EMPLOYEE_NOT_FOUND)
            return make_response(EMPLOYEE_NOT_FOUND), HTTPStatus.BAD_REQUEST

        employee.update(params)
        logger.info("Employee updated successfully.")
        return make_response("Employee record updated successfully."), HTTPStatus.OK

    except Exception as e:
        logger.error(str(e))
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST
    


# internal api for fake inserts of employee records
@employee_bp.route('/fake', methods=['GET'])
def fake_inserts():
    cursor = g.db.cursor()

    query = '''INSERT INTO Employee(_id, first_name, last_name, email, password, phone, designation)
                    VALUES (%(_id)s, %(first_name)s, %(last_name)s, %(email)s, %(password)s, %(phone)s, %(designation)s)'''

    id = 3000
    phone = 9000000000

    for i in range(3000, 5000):
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