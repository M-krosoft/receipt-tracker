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
            f"  SQLALCHEMY_DATABASE_URI : '{self.SQLALCHEMY_DATABASE_URI}'\n"
            f"  SECRET_KEY: '{self.SECRET_KEY}'\n"
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
