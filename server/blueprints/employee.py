from flask import Blueprint, jsonify, request


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
    pass


@employee_bp.route('/<int:id>', methods=['PUT'])
def update_employee():
    pass


@employee_bp.route('/<int:id>', methods=['DELETE'])
def delete_employee():
    pass
