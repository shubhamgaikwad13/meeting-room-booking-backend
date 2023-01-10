class Teams:
    __tablename__: 'Team'

    def __init__(self, id, name):
        self.id = id
        self.name = name

    @staticmethod
    def get_teams(teams):
        teamsList = []
        for team in teams:
            team = {
                'TeamName': team[0],
                'Members': team[1]
            }
            teamsList.append(team)
        return teamsList

    @staticmethod
    def get_team(team):
        if team[0]:
            teams_dict = {
                'TeamName': team[0],
                'Members': team[1]
            }
            return teams_dict
        return None
