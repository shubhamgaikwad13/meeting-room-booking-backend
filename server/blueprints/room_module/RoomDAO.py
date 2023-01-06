import json

class Room:
    __tablename__: 'Room'
 
    def __init__(self ,id , title , type, capacity, description, has_microphone, has_projector, has_speakers, has_whiteboard):
 
        self.id = id
        self.title = title
        self.type = type
        self.capacity = capacity
        self.description = description
        self.has_microphone = has_microphone
        self.has_projector = has_projector
        self.has_speakers = has_speakers
        self.has_whiteboard = has_whiteboard
 
    @staticmethod
    def get_room(room):
        return json.dumps(room,default=str)

    # @staticmethod
    # def get_rooms(room):
