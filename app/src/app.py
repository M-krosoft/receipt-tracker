import logging

from flask import Flask

from config import DevelopmentConfig

config = DevelopmentConfig()
logger = logging.getLogger(__name__)


def setup_logging_level():
    if config.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)


def create_app():
    setup_logging_level()
    logger.info("creating app...")
    logger.debug(f"config=\n {str(config)}")

    app = Flask(__name__)
    app.config.from_object(config)

    return app
