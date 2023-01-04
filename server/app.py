from flask import Flask
from .blueprints.employee_module.employee import employee_bp


app = Flask(__name__)

app.register_blueprint(employee_bp)


@app.route("/")
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
