import os


class Config:
    DEBUG = False
    TESTING = False
    DATABASE_URL = ''
    DATABASE_USERNAME = ''
    DATABASE_PASSWORD = ''
    SECRET_KEY = ''

    def __str__(self):
        return (
            f"Config:\n"
            f"  DEBUG: {self.DEBUG}\n"
            f"  DATABASE_URL: '{self.DATABASE_URL}'\n"
            f"  DATABASE_USERNAME: '{self.DATABASE_USERNAME}'\n"
            f"  DATABASE_PASSWORD: '{self.DATABASE_PASSWORD}'\n"
            f"  SECRET_KEY: '{self.SECRET_KEY}'\n"
        )


class DevelopmentConfig(Config):
    DEBUG = True
    DATABASE_URL = 'jdbc:postgresql://localhost:5432/receipt_tracker'
    DATABASE_USERNAME = 'receipt_tracker'
    DATABASE_PASSWORD = 'receipt_tracker'
    SECRET_KEY = ''


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    DATABASE_URL = os.environ.get('DATABASE_URL')
    DATABASE_USERNAME = os.environ.get('DATABASE_USERNAME')
    DATABASE_PASSWORD = os.environ.get('DATABASE_PASSWORD')
    SECRET_KEY = os.environ.get('SECRET_KEY')


class TestingConfig(Config):
    TESTING = True
    DEBUG = True
    DATABASE_URL = "sqlite:///testdb.sqlite"
