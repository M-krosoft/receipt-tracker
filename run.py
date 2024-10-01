from app import create_app

app = create_app()


@app.route('/isRunning')
def home():
    return "Application is running!"


if __name__ == '__main__':
    app.run(debug=True)
