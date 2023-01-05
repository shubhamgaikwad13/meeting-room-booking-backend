from ...utils import field_must_be_type, field_required
from .constant import *

EmployeeFields = {
    '_id': {'is_required': True, 'type': str},
    'first_name': {'is_required': True, 'type': str},
    'last_name': {'is_required': True, 'type': str},
    'phone': {'is_required': True, 'type': str},
    'email': {'is_required': True, 'type': str},
    'password': {'is_required': True, 'type': str},
    'designation': {'is_required': True, 'type': str},
    'is_admin': {'is_required': True, 'type': bool}
}


class EmployeeValidation:
    # common validations for employee fields
    @staticmethod
    def validate(params):
        # checks if field is required and type is valid or not otherwise raises exception
        for key, value in EmployeeFields.items():

            # if field is required but not passed in request
            if value['is_required'] and params.get(key) is None:
                raise Exception(field_required(key))

            # checks type of field
            if type(params.get(key)) is not value['type']:
                raise Exception(f"{key} must be of type {value['type']}")

            # phone validations
            if key == 'phone':
                EmployeeValidation.validate_phone(params['phone'])

    @staticmethod
    def validate_phone(phone):
        # validate phone
        if len(str(phone)) != 10:
            raise Exception(EMPLOYEE_PHONE_LENGTH)
        if not phone.isdigit():
            raise Exception(EMPLOYEE_PHONE_INVALID)
