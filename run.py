from flask import jsonify
from sqlalchemy import text

from app import create_app, db
from app.config import DevelopmentConfig

config = DevelopmentConfig()
app = create_app(config)


@app.route('/isRunning')
def home():
    return "Application is running!"


@app.route('/test_connection', methods=['GET'])
def test_db_connection():
    with app.app_context():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify({"status": "success", "message": "Connected to the database!"}), 200
        except Exception as e:
            return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run()
