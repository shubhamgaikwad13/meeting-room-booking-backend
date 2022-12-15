from flask import Flask
from .blueprints import employee
from .blueprints.teams_module import teams

app = Flask(__name__)

app.register_blueprint(employee.employee_bp)
app.register_blueprint(teams.team_bp)


@app.route("/")
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
