import json

class Meeting:
    __tablename__:'Meeting'
    
    def __init__(self, _id, title, date, start_time, end_time, summary, room_id):
        self._id = _id
        self.title = title
        self.date = date
        self.start_time = start_time,
        self.end_time = end_time,
        self.summary = summary,
        self.room_id = room_id
        
    @staticmethod
    def get_meetings(meetings):
        data = []
        for index in meetings:
            meetings_dict = {
                '_id' : index[0],
                'title' : index[1],
                'date' : index[2],
                'start_time' : index[3],
                'end_time' : index[4],
                'summary' : index[5],
                'room_id' : index[6]
            }
            data.append(meetings_dict)
        
        return json.dumps(data)
    
    @staticmethod
    def get_meeting(meeting):
        return json.dumps(meeting, default=str)
        

 
class MeetingMember:
    __tablename__: 'MeetingMember'
    
    def __init__(self, _id, meeting_id, team_id, attendee_id):
        self._id = _id
        self.meeting_id = meeting_id
        self.team_id = team_id
        self.attendee_id = attendee_id
        
    