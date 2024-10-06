from flask import jsonify
from sqlalchemy import text

from app import create_app, db
from app.app_config import DevelopmentConfig
from flask_migrate import Migrate

from dotenv import load_dotenv

load_dotenv()

config = DevelopmentConfig()
app = create_app(config)

migrate = Migrate(app, db)


@app.route('/isRunning')
def home():
    return "Application is running!"


@app.route('/test_connection', methods=['GET'])
def db_connection_test():
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "success", "message": "Connected to the database!"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(port=5000)
