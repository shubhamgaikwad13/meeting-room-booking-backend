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
import logging

room_bp = Blueprint('room', __name__, url_prefix='/room')
logger = logging.getLogger("room_module")

@room_bp.route('/', methods=['POST'])
def add_room():
    params = request.get_json()
    logger.info("Adding a new room.")

    try:
        # validates request parameters and throws exception for invalid params
        logger.info("Validating add request parameters.")
        RoomValidation.validate(params)

        # checks if request is being made by admin
        logger.info("Checking if only admin is adding the room.")
        if not Employee.is_admin(params['created_by']):
            raise Exception(ONLY_ADMIN_ADDS_ROOM)

        room = Room(**params)
        logger.info("Inserting room record in the database.")
        room.save()  # inserts room record in the database

    except MySQLError as err:
        logger.error(str(err))
        # Error handling for duplicate entries for title
        if err.errno == errorcode.ER_DUP_ENTRY:
            for key in DUP_ENTRY:
                if key in err.msg:
                    return make_response(dup_message(key), 'error'), HTTPStatus.BAD_REQUEST

        # Other mysql errors
        return make_response(str(err), 'error'), HTTPStatus.BAD_REQUEST

    except Exception as e:
        logger.error(str(e))
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    logger.info(ROOM_ADDED)
    return make_response(ROOM_ADDED), HTTPStatus.OK



@room_bp.route('/', methods=['GET'])
def get_rooms():
    logger.info("Fetching all rooms.")
    try:
        rooms = Room.get_rooms()  # fetches rooms in list
        if rooms:
            logger.info("All rooms fetched successfully.")
            return make_response(rooms, key="rooms"), HTTPStatus.OK

        logger.info(NO_ROOMS_FOUND)
        return make_response(NO_ROOMS_FOUND), HTTPStatus.OK
    except Exception as e:
        logger.error(str(e))
        return make_response(FETCH_ROOMS_FAILED, key="error"), HTTPStatus.BAD_REQUEST



@room_bp.route('/<id>', methods=['GET'])
def get_room_by_id(id):
    logger.info(f"Fetching room with id {id}")
    try:
        room = Room.get_room_by_id(id)  # fetches room in object

        if room is None:
            logger.info(ROOM_NOT_FOUND)
            return make_response(ROOM_NOT_FOUND), HTTPStatus.OK

        logger.info("Room fetched successfully.")
        return make_response(data=room, key='room'), HTTPStatus.OK

    except Exception as e:
        logger.error(str(e))
        return make_response(data=str(e), key="error"), HTTPStatus.BAD_REQUEST


@room_bp.route('/<id>', methods=['DELETE'])
def delete_room_by_id(id):
    logger.info("Deleting the room.")
    try:
        params = request.get_json()

        # checks if request is being made by admin
        logger.info("Checking if only admin is deleting the room.")
        if not Employee.is_admin(params['updated_by']):
            raise Exception("Only admin can delete the room.")

        # if room exists then deletes otherwise shows error
        logger.info("Checking if room exists in the database.")
        room = Room.get_room_by_id(id)

        if room is None:
            logger.info(ROOM_NOT_FOUND)
            return make_response(ROOM_NOT_FOUND), HTTPStatus.BAD_REQUEST
        
        logger.info("Deleting room record in the database.")
        room.delete()  # if room exists then deletes its record

    except Exception as e:
        logger.error(str(e))
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST

    logger.info("Room deleted succesfully.")
    return make_response(ROOM_DELETED), HTTPStatus.OK



@room_bp.route('/<id>', methods=['PATCH'])
def update_room_by_id(id):
    params = request.get_json()
    logger.info(f"Updating an room {id}")

    try:
        RoomValidation.validate_update_request(params)

        # checks if request is being made by admin
        logger.info("Checking if only admin is updating the room.")
        if not Employee.is_admin(params['updated_by']):
            raise Exception(ONLY_ADMIN_UPDATES_ROOM)
        
        # if room exists then updates otherwise shows error
        logger.info("Checking if room exists in the database.")
        room = Room.get_room_by_id(id)
        if room is None:
            logger.info(ROOM_NOT_FOUND)
            return make_response(ROOM_NOT_FOUND), HTTPStatus.BAD_REQUEST

        room.update(params)
        logger.info("Room updated successfully.")
        return make_response("Room record updated successfully."), HTTPStatus.OK

    except Exception as e:
        logger.error(str(e))
        return make_response(str(e), 'error'), HTTPStatus.BAD_REQUEST