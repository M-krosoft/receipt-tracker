import logging

from flask import Flask
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

    db.init_app(_app)
    with _app.app_context():
        db.create_all()

    return _app


def setup_logging_level(config: Config):
    if config.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)
