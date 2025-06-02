import os
from dotenv import load_dotenv
from flask import Flask
from app.logger import logger

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY", default="secret")

    from . import routes

    app.register_blueprint(routes.bp)

    logger.info("Application initialized")
    return app
