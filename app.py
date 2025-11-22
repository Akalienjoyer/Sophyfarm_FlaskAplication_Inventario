from flask import Flask, request, jsonify
from config import Config
from flask_migrate import Migrate
from flask_cors import CORS
from models.db import db
from controllers.elemento_controller import elemento_bp
from controllers.movimientos_controller import movimientos_bp
from controllers.test_controller import test_bp
from models.tipomov import TipoMov
from models.movimiento import Movimiento
from models.elemento import Elemento
from flasgger import Swagger
from controllers.reportes_controller import reportes_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    
    # CORS — CONFIGURACIÓN CORRECTA
    CORS(app, origins=["http://localhost:5173"], supports_credentials=True)

    app.config.from_object(config_class)
    Swagger(app)

    # Inicializar DB y migraciones
    db.init_app(app)
    migrate = Migrate(app, db)

    # Blueprints
    app.register_blueprint(test_bp, url_prefix="/api/test")
    app.register_blueprint(elemento_bp, url_prefix="/api/elementos")
    app.register_blueprint(movimientos_bp, url_prefix="/api/movimientos")
    app.register_blueprint(reportes_bp)

    @app.route("/")
    def index():
        return {"service": "inventario", "version": "1.0"}, 200

    # =========================
    #        LOGIN API
    # =========================
    

    return app
