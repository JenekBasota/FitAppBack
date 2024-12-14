from flask import Flask, current_app, send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from sqlalchemy.orm import sessionmaker
from utils import dbConnectionEngine
from routes import auth_Blueprint, jwt_Blueprint, swaggerui_blueprint

def create_app():
    # Создаем Flask приложение
    app = Flask(__name__)

    # Загружаем переменные окружения из .env файла
    load_dotenv()

    # Настройки приложения
    app.config["SECRET_KEY"] = os.urandom(64)
    app.config["JWT_SECRET_KEY"] = os.urandom(64)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]

    # Инициализация расширений
    cors = CORS()
    jwt = JWTManager()

    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    jwt.init_app(app)

    # Настройка контекста приложения
    def setup_app_context():
        with app.app_context():
            current_app.session_bd = sessionmaker(
                bind=dbConnectionEngine().get_engine().connect()
            )()

    # Вызов функции для настройки контекста
    setup_app_context()

    # Регистрируем blueprints
    app.register_blueprint(auth_Blueprint, url_prefix="/api/auth")
    app.register_blueprint(jwt_Blueprint, url_prefix="/api/jwt")
    app.register_blueprint(swaggerui_blueprint)

    # Маршрут для теста
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    # Маршрут для swagger.json
    @app.route("/docs/swagger.json")
    def send_docs():
        return send_from_directory(
            os.path.join(app.root_path, "routes", "swagger", "docs"), "swagger.json"
        )

    return app
