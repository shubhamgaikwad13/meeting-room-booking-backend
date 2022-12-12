from flask import Flask
from .blueprints import employee


app = Flask(__name__)

app.register_blueprint(employee.employee_bp)


@app.route("/")
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
