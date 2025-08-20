# __init__.py
from flask import Flask, redirect, send_from_directory
from config import Config
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from .models import db
from flask_cors import CORS


def initialize_app():
    app = Flask(__name__)
    # CORS(app)
    CORS(app, resources={r"/*": {"origins": ["http://localhost:3000","http://localhost:5000", "http://127.0.0.1:3000", "http://127.0.0.1:5000", "http://192.168.31.147:3000"]}})
    
    # CORS(app, resources={r"/*": {"origins": "*"}})
    # cors = CORS()
    # cors.init_app(app, resources={r"/*": {"origins": "*"}})
   # CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

    # App Config
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['JWT_SECRET_KEY'] = 'personal-finance'
    app.config['CIPHER_KEY'] = Config.CIPHER_KEY

    # Initialize JWT and DB
    JWTManager(app)
    # CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True, allow_headers=["Content-Type", "Authorization"])
    db.init_app(app)

    # Swagger
    SWAGGER_URL = '/api/docs'
    API_URL = '/swagger/swagger.json'
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "Personal Finance", 'deepLinking': True, 'layout': "BaseLayout",  # 👈 Enables top bar
                'docExpansion': "none"}
    )
    app.register_blueprint(swaggerui_blueprint)

    # Swagger file access
    @app.route('/swagger/<path:path>')
    def send_static(path):
        return send_from_directory('swagger', path)

    # Root redirect to docs
    @app.route('/')
    def redirect_to_docs():
        return redirect(SWAGGER_URL)

    # Blueprints
    from app.api.controller.asset import assets_bp
    from app.api.controller.users import users_bp
    from app.api.controller.constants import constants_bp
    from app.api.controller.pwd import pwd_bp
    app.register_blueprint(assets_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(constants_bp)
    app.register_blueprint(pwd_bp)

    return app
