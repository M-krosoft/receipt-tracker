import logging

from flask import Flask
from flask.sansio.blueprints import Blueprint
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .app_config import Config

logger = logging.getLogger(__name__)
db = SQLAlchemy()


def create_app(config: Config):
    setup_logging_level(config)
    logger.info("creating app...")
    logger.debug(f"config=\n {str(config)}")

    _app = Flask(__name__)
    _app.config.from_object(config)

    JWTManager(_app)

    auth_bp = _prepare_authentication()
    _app.register_blueprint(auth_bp)

    db.init_app(_app)
    with _app.app_context():
        db.create_all()

    return _app


def setup_logging_level(config: Config):
    if config.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def _prepare_authentication() -> Blueprint:
    from .controllers.auth_controller import AuthController
    from .repositories.user_repository import UserRepository
    from .services.auth_service import AuthService

    user_repository = UserRepository()
    auth_service = AuthService(user_repository)
    auth_controller = AuthController(auth_service)

    return auth_controller.create_blueprint()
