from flask import Flask, g
from .config import ProductionConfig, TestingConfig, DevelopmentConfig
import logging
import os
from flask_jwt_extended import JWTManager, get_jwt, get_jwt_identity, set_access_cookies, create_access_token
from .db import connect_db
from datetime import datetime, timedelta, timezone
from .blueprints.auth_module.controller import auth_bp
from .blueprints.employee_module.controller import employee_bp
from .blueprints.room_module.controller import room_bp
import logging

logger = logging.getLogger("app_logger")

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

    
    # jwt configuration
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_KEY")
    app.config["JWT_COOKIE_SECURE"] = False
    app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)

    JWTManager(app)


    # db connection
    @app.before_request
    def before_request():
        logger.info("Connected to db.")
        g.db = connect_db()
        

    @app.after_request
    def after_request(response):
        logger.info("Connection to db closed.")
        g.db.close()
        return response

    @app.after_request
    def refresh_expiring_jwts(response):
        try:
            exp_timestamp = get_jwt()["exp"]
            now = datetime.now(timezone.utc)
            target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
            if target_timestamp > exp_timestamp:
                access_token = create_access_token(identity=get_jwt_identity())
                set_access_cookies(response, access_token)
            return response
        except (RuntimeError, KeyError):
            # Case where there is not a valid JWT. Just return the original response
            return response

    #register new blueprints here
    app.register_blueprint(employee_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(room_bp)
    
    return app
