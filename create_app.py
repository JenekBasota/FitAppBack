from flask import Flask, current_app, send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import os
from sqlalchemy.orm import sessionmaker
from utils import dbConnectionEngine
from routes import auth_Blueprint, jwt_Blueprint, swaggerui_blueprint
from models import Base  # Импортируем базовый класс для создания таблиц

def create_app():
    
    app = Flask(__name__)
    cors = CORS()
    jwt = JWTManager()

    load_dotenv()
    database_url = os.getenv('sqlite:///test.db')

    def setup_app_context():
        with app.app_context():
            engine = dbConnectionEngine(database_url).get_engine()
            current_app.session_bd = sessionmaker(bind=engine)()
            Base.metadata.create_all(engine)  # Создаем таблицы

    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route("/docs/swagger.json")
    def send_docs():
        return send_from_directory(
            os.path.join(app.root_path, "routes", "swagger", "docs"), "swagger.json"
        )

    app.config["SECRET_KEY"] = os.urandom(64)
    app.config["JWT_SECRET_KEY"] = os.urandom(64)
    app.config["JWT_TOKEN_LOCATION"] = ["headers"]
    setup_app_context()

    app.register_blueprint(auth_Blueprint, url_prefix="/api/auth")
    app.register_blueprint(jwt_Blueprint, url_prefix="/api/jwt")
    app.register_blueprint(swaggerui_blueprint)

    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})
    
    return app
