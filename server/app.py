from flask import Flask
from dotenv import load_dotenv
import os
from .blueprints.auth_module import auth_bp

app = Flask(__name__)

app.register_blueprint(auth_bp.login_bp)

dotenv_path = '.env'
load_dotenv(dotenv_path)

app.config["SECRET_KEY"] = os.environ.get("JWT_KEY")
# print("jwt", os.environ.get("JWT_KEY"))




@app.route("/")
def hello_world():
    return "Hello, world!"


if __name__ == "__main__":
    app.run()
