from flask import Flask
from .config import ProductionConfig, TestingConfig, DevelopmentConfig
from .blueprints.employee_module import controller
import logging
import os
from .blueprints.auth_module import login_bp
from flask_jwt_extended import JWTManager


def create_app(test_config=None):
    logging.basicConfig(filename='app.log', filemode='a', level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    if app.config["ENV"] == 'production':
        app.config.from_object(ProductionConfig())
    elif app.config["ENV"] == 'testing':
        app.config.from_object(TestingConfig())
    else:
        app.config.from_object(DevelopmentConfig())

    if app.debug:
        # Fix werkzeug handler in debug mode
        logging.getLogger('werkzeug').disabled = True

    app.register_blueprint(controller.employee_bp)
    app.register_blueprint(login_bp.login_bp)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_KEY")
    JWTManager(app)

    return app
