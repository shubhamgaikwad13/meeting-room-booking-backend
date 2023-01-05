from flask import Flask
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager

from .blueprints.auth_module import auth_bp
from .blueprints.employee import employee_bp

app = Flask(__name__)


app.register_blueprint(auth_bp.login_bp)
app.register_blueprint(employee_bp)
dotenv_path = '.env'
load_dotenv(dotenv_path)

app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_KEY")
# print("jwt", os.environ.get("JWT_KEY"))


JWTManager(app)


@app.route("/")
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
