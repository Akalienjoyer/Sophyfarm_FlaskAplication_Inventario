from flask import Flask
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from models.db import db
from controllers.elemento_controller import elemento_bp
from controllers.movimientos_controller import movimientos_bp
from controllers.test_controller import test_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    CORS(app)

    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprints (rutas)
    app.register_blueprint(test_bp, url_prefix="/api/test")
    app.register_blueprint(elemento_bp, url_prefix='/api/elementos')
    app.register_blueprint(movimientos_bp, url_prefix='/api/movimientos')

    @app.route('/')
    def index():
        return {"service": "inventario", "version": "1.0"}, 200

    return app
