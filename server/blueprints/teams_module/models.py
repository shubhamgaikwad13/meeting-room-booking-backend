import json

class Teams:
    __tablename__: 'Team'

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get_teams(teams):
        data = []
        for team in teams:
            teams_dict = {
                'name': team[0],
                'members':team[1]
            }
            data.append(teams_dict)
        return json.dumps(data)





