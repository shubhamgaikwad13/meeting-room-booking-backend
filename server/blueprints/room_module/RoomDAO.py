from flask import g
from .constant import *
class Room:
    __tablename__: 'Room'
 
    def __init__(self,_id=None, title=None, type='meeting', capacity=None, description=None, has_microphone=False, has_projector=False, has_speakers=False, has_whiteboard=False, created_by=None): 
        self._id = _id
        self.title = title
        self.type = type
        self.description = description
        self.capacity = capacity
        self.has_microphone = has_microphone
        self.has_projector = has_projector
        self.has_speakers = has_speakers
        self.has_whiteboard = has_whiteboard
        self.created_by = created_by
 
    @staticmethod
    def get_room_by_id(room_id):
        """Fetches room by id 

        Returns:
            object: Room 
        """
        cursor = g.db.cursor()

        query = '''SELECT * FROM Room WHERE _id = %(_id)s'''
        params = {'_id': room_id}
        cursor.execute(query, params)

        record = cursor.fetchone()
        if record:
            print("rec", record)
            room = Room(*record[:9])
            print(room.__dict__)
            return room


    @staticmethod
    def get_rooms():
        """Fetches all rooms from the database

        Returns:
            list: List of rooms with each room as a dictionary
        """
        cursor = g.db.cursor()
        query = '''SELECT * FROM Room'''
        cursor.execute(query)
        records = cursor.fetchall()
        rooms = []
        for room_record in records:
            room = Room(*room_record[:9])
            rooms.append(room.__dict__)

        return rooms
        
    def delete(self):
        """Deletes room record from the database by matching on room id"""

        cursor = g.db.cursor()

        query = '''DELETE FROM Room WHERE  _id=%(_id)s'''
        params = {'_id': self._id}
        cursor.execute(query, params)
        g.db.commit()


    def save(self):
        """Inserts room record in the database"""

        cursor = g.db.cursor()

        query = '''INSERT INTO Room(title, type, capacity, description, has_microphone, has_projector, has_speakers, has_whiteboard, created_by)
                VALUES (%(title)s, %(type)s, %(capacity)s, %(description)s, %(has_microphone)s, %(has_projector)s, %(has_speakers)s, %(has_whiteboard)s, %(created_by)s)'''
        cursor.execute(query, self.__dict__)
        g.db.commit()

    
    def update(self, params):
        """Updates room record"""
    
        cursor = g.db.cursor()

        # forms update query based on fields to be updated
        query = '''UPDATE Room SET '''

        for field in self.__dict__.keys():
            if field in params:
                self.__dict__[field] = params[field]
                query = query + f'{field}=%({field})s,'

        query = query[:-1] + f' WHERE _id=%(_id)s'

        cursor.execute(query, self.__dict__)
        g.db.commit()