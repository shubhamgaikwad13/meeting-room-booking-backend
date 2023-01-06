from flask import Blueprint, jsonify, request
from ..db import connect_db
from ..models import Room


room_bp = Blueprint('room', __name__, url_prefix='/room')


@room_bp.route('/', methods=['POST'])
def add_room():
    db = connect_db()
    cursor = db.cursor()

    query = '''INSERT INTO Room(title , type, capacity, description, has_microphone, has_projector, has_speakers, has_whiteboard)
                VALUES ( %(title)s, %(type)s, %(capacity)s, %(description)s, %(has_microphone)s, %(has_projector)s, %(has_speakers)s,%(has_whiteboard)s)'''

    try:

        cursor.execute(query, request.get_json())
        db.commit()
        return "Added Succesfully"
    except Exception as e:
        print(e)
        print('Failed to insert record')
        return "Failed to Post Data"


@room_bp.route('/', methods=['GET'])
def get_rooms():
    db = connect_db()
    cursor = db.cursor()

    query = '''SELECT * FROM Room'''

    try:
        cursor.execute(query)

        data = cursor.fetchall()
        print(data)

        print(type(data))
        return jsonify(data)
    except:
        print('Failed to insert record')
        return "Error"


@room_bp.route('/<id>', methods=['GET'])
def get_room_byId(id):
    db = connect_db()
    cursor = db.cursor()

    query = '''SELECT * FROM Room WHERE  _id = %(_id)s'''

    try:
        # print(query)
        cursor.execute(query, {"_id": id})

        data = cursor.fetchone()

        # print("hello", Room.get_room(data))
        return jsonify(data)
    except:
        print('Failed to get record')
        return "Error"


@room_bp.route('/<id>', methods=['DELETE'])
def delete_room_byId(id):
    db = connect_db()
    cursor = db.cursor()

    query = '''DELETE FROM Room WHERE  _id=%(_id)s'''

    try:
        cursor.execute(query, {"_id": id})

        db.commit()
        return "202"
    except:
        print('Failed to delete record')
        return "404"


@room_bp.route('/<id>', methods=['PATCH'])
def edit_room_byId(id):
    db = connect_db()
    cursor = db.cursor()

    query = '''UPDATE Room SET '''
    for field in request.get_json().keys():
        query = query+f'{field} = %({field})s,'
    query = query[:-1] + f' WHERE  _id=%(_id)s'

    try:
        print(query)
        cursor.execute(query, {**request.get_json(),'_id': id}
        )

        db.commit()
        return "202"
    except Exception as e:
        print(e)
        print('Failed to edit record')
        return "404"