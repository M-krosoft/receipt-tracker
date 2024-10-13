from dotenv import load_dotenv

from app import create_app
from app.app_config import create_config

load_dotenv()

config = create_config()
app = create_app(config)

if __name__ == '__main__':
    app.run(port=5000)
