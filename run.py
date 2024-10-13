from dotenv import load_dotenv
from flask import jsonify
from flask_jwt_extended import jwt_required
from sqlalchemy import text

from app import create_app, db
from app.app_config import create_config

load_dotenv()

config = create_config()
app = create_app(config)


@app.route('/isRunning')
def home():
    return "Application is running!"


@app.route('/protected')
@jwt_required()
def protected():
    return "You reached protected endpoint!"


@app.route('/unprotected')
def unprotected():
    return "You reached unprotected endpoint!"


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
