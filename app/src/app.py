from flask import Flask

app = Flask(__name__)


@app.route('/isRunning')
def home():
    return "Application is running test!"


if __name__ == '__main__':
    app.run(debug=True)
