from flask import Blueprint, request, g, jsonify
from http import HTTPStatus
from .RoomDAO import Room
from .service import RoomValidation
from flask_jwt_extended import jwt_required
from .constant import *
from mysql.connector import errorcode
from mysql.connector import Error as MySQLError
from ...utils import make_response, dup_message
from ..employee_module.EmployeeDAO import Employee

room_bp = Blueprint('room', __name__, url_prefix='/room')


@room_bp.route('/', methods=['POST'])
def add_room():
    params = request.get_json()

    try:
        # validates request parameters and throws exception for invalid params
        RoomValidation.validate(params)

        # checks if request is being made by admin
        if not Employee.is_admin(params['created_by']):
            raise Exception(ONLY_ADMIN_ADDS_ROOM)

        room = Room(**params)
        room.save()  # inserts room record in the database

    except MySQLError as err:
        # Error handling for duplicate entries for title
        if err.errno == errorcode.ER_DUP_ENTRY:
            for key in DUP_ENTRY:
                if key in err.msg:
                    return make_response(dup_message(key), 'error'), HTTPStatus.BAD_REQUEST

        # Other mysql errors
        return make_response(str(err), 'error'), HTTPStatus.BAD_REQUEST

    except Exception as e:
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    return make_response(ROOM_ADDED), HTTPStatus.OK



@room_bp.route('/', methods=['GET'])
def get_rooms():
    try:
        rooms = Room.get_rooms()  # fetches rooms in list
        if rooms:
            return make_response(rooms, key="rooms"), HTTPStatus.OK

        return make_response(NO_ROOMS_FOUND), HTTPStatus.OK
    except Exception as e:
        return make_response(FETCH_ROOMS_FAILED, key="error"), HTTPStatus.BAD_REQUEST



@room_bp.route('/<id>', methods=['GET'])
def get_room_by_id(id):
    try:
        room = Room.get_room_by_id(id)  # fetches room in object

        if room is None:
            return make_response(ROOM_NOT_FOUND), HTTPStatus.OK

        return make_response(data=room.__dict__, key='room'), HTTPStatus.OK

    except Exception as e:
        return make_response(data=str(e), key="error"), HTTPStatus.BAD_REQUEST


@room_bp.route('/<id>', methods=['DELETE'])
def delete_room_by_id(id):
    try:
        params = request.get_json()

        # checks if request is being made by admin
        if not Employee.is_admin(params['updated_by']):
            raise Exception("Only admin can delete the room.")

        # if room exists then deletes otherwise shows error
        room = Room.get_room_by_id(id)

        if room is None:
            return make_response(ROOM_NOT_FOUND), HTTPStatus.BAD_REQUEST

        room.delete()  # if room exists then deletes its record

    except Exception as e:
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    return make_response(ROOM_DELETED), HTTPStatus.OK



@room_bp.route('/<id>', methods=['PATCH'])
def update_room_by_id(id):
    params = request.get_json()

    try:
        RoomValidation.validate_update_request(params)

        # checks if request is being made by admin
        if not Employee.is_admin(params['updated_by']):
            raise Exception(ONLY_ADMIN_UPDATES_ROOM)
        
        # if employee exists then updates otherwise shows error
        room = Room.get_room_by_id(id)
        if room is None:
            return make_response(ROOM_NOT_FOUND), HTTPStatus.BAD_REQUEST

        room.update(params)
        return make_response("Room record updated successfully."), HTTPStatus.OK

    except Exception as e:
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST