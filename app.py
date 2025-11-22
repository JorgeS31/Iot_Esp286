from flask import Flask, jsonify
from flask_cors import CORS
from database import Database
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    # CORS abierto para cualquier origen en /api/*
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    )

    try:
        # Inicializar pool de conexiones
        Database.init_pool()
        logger.info("✅ Pool de base de datos inicializado correctamente")
    except Exception as e:
        logger.error(f"❌ Error al inicializar el pool de BD: {e}")
        # No detenemos la app, pero logueamos el error

    # Registrar blueprints (con manejo de errores)
    try:
        from controllers.iot_device_controller import iot_devices_bp
        app.register_blueprint(iot_devices_bp)
        logger.info("✅ Blueprint de dispositivos IoT registrado")
    except ImportError as e:
        logger.warning(f"⚠️ Blueprint no encontrado: {e}")
    except Exception as e:
        logger.error(f"❌ Error registrando blueprint: {e}")

    @app.route("/api/health", methods=["GET"])
    def health():
        try:
            # Verificar conexión a BD si está inicializada
            if hasattr(Database, '_pool') and Database._pool:
                connection = Database.get_connection()
                Database.return_connection(connection)
                db_status = "connected"
            else:
                db_status = "pool_not_initialized"

            return jsonify({
                "status": "ok",
                "database": db_status,
                "message": "IoT API running successfully"
            }), 200
        except Exception as e:
            return jsonify({
                "status": "error",
                "database": "disconnected",
                "error": str(e)
            }), 500

    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "message": "Bienvenido a la API IoT",
            "version": "1.0",
            "endpoints": {
                "health": "/api/health",
                "devices": "/api/devices"
            }
        })

    return app


if __name__ == "__main__":
    app = create_app()
    logger.info("🚀 Iniciando servidor IoT API en http://0.0.0.0:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)