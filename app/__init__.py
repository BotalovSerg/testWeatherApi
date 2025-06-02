from flask import Flask
from app.logger import logger


def create_app():
    app = Flask(__name__)
    app.secret_key = "secret"  # Для разработки, в продакшене через переменные окружения

    from . import routes
    app.register_blueprint(routes.bp)

    logger.info("Application initialized")
    return app
