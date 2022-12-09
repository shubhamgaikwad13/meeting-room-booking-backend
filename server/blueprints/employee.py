from flask import Blueprint, jsonify, request

employee_bp = Blueprint('employee', __name__, url_prefix='/employee')


@employee_bp.route('/', method=['GET'])
def get_employees():
    output = {'msg': 'hi employee'}
    return jsonify(output)
