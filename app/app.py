import logging

from flask import Flask, Blueprint
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from .app_config import Config

logger = logging.getLogger(__name__)
db = SQLAlchemy()
jwt = JWTManager()


def create_app(config: Config):
    setup_logging_level(config)
    logger.info("creating app...")
    logger.debug(f"config=\n {str(config)}")

    _app = Flask(__name__)
    _app.config.from_object(config)

    main_bp = Blueprint('main', __name__, url_prefix='/receipt-tracker')
    auth_bp = _prepare_authentication()
    main_bp.register_blueprint(auth_bp)

    _app.register_blueprint(main_bp)

    db.init_app(_app)
    jwt.init_app(_app)
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
