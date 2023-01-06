from ...utils import field_must_be_type, field_required
from .constant import *

RoomFields = {
    'title': {'is_required': True, 'type': str},
    'type': {'is_required': False, 'type': str},
    'capacity': {'is_required': True, 'type': int},
    'description': {'is_required': False, 'type': str},
    'has_microphone': {'is_required': True, 'type': bool},
    'has_projector': {'is_required': True, 'type': bool},
    'has_speakers': {'is_required': True, 'type': bool},
    'has_whiteboard': {'is_required': True, 'type': bool},
    'created_by': {'is_required': True, 'type': str},
    'updated_by': {'is_required': False, 'type': str}
}

class RoomValidation:
    @staticmethod
    def validate(params):
        # checks if field is required and type is valid or not otherwise raises exception
        for key, value in RoomFields.items():

            # if field is required but not passed in request
            if value['is_required'] and params.get(key) is None:
                raise Exception(field_required(key))

            # checks type of field
            if value['is_required'] and type(params.get(key)) is not value['type']:
                raise Exception(f"{key} must be of type {value['type']}")


    @staticmethod
    def validate_update_request(params):
        for key, value in params.items():
            required_type = RoomFields[key]['type']
            if  type(value) is not required_type:
                raise Exception(f"{key} must be of type {required_type}")
