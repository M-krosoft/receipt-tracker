import os


class Config:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = ''
    SECRET_KEY = '2afbfac8fe49058f12874b6c7f92d6c842d2ec05f621f9b3b4ba437eb8f7b338'
    APPLICATION_ROOT = '/receipt-tracker'

    def __str__(self):
        return (
            f"Config:\n"
            f"  DEBUG: {self.DEBUG}\n"
            f"  TESTING: {self.TESTING}\n"
            f"  SQLALCHEMY_DATABASE_URI : '{self.SQLALCHEMY_DATABASE_URI}'\n"
            f"  SECRET_KEY: '{self.SECRET_KEY}'\n"
            f" APPLICATION_ROOT: '{self.APPLICATION_ROOT}'\n"
        )


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://receipt_tracker:receipt_tracker@localhost:5432/receipt_tracker'
    SECRET_KEY = ''


class DevelopmentSqliteConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///receipt-tracker.db'
    SECRET_KEY = '2afbfac8fe49058f12874b6c7f92d6c842d2ec05f621f9b3b4ba437eb8f7b338'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI ')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


def create_config():
    config_mode = os.getenv("CONFIG_MODE")
    if config_mode == "development":
        return DevelopmentConfig()
    if config_mode == "production":
        return ProductionConfig()
    if config_mode == "testing":
        return TestingConfig()
    if config_mode == "sqlite":
        return DevelopmentSqliteConfig()
