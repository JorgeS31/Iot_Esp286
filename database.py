import mysql.connector
from mysql.connector import pooling

class Config:
    # Configuración del pool de conexiones
    POOL_NAME = "mypool"
    POOL_SIZE = 5  # puedes ajustar este valor

    # Datos de conexión a tu base de datos (CON PORT AGREGADO)
    DB_CONFIG = {
        "host": "instancia-iot-rds.cja06eu6ednb.us-east-1.rds.amazonaws.com",
        "port": 3306,  # ← ¡IMPORTANTE! Agregar el puerto
        "user": "admin",
        "password": "Admin12345#!",
        "database": "iot_db"
    }

class Database:
    _pool = None

    @classmethod
    def init_pool(cls):
        if cls._pool is None:
            try:
                print(f"🔗 Intentando conectar a: {Config.DB_CONFIG['host']}")
                cls._pool = pooling.MySQLConnectionPool(
                    pool_name=Config.POOL_NAME,
                    pool_size=Config.POOL_SIZE,
                    **Config.DB_CONFIG
                )
                print("✅ Pool de conexiones inicializado exitosamente!")
            except Exception as e:
                print(f"❌ Error al inicializar pool: {e}")
                raise e

    @classmethod
    def get_connection(cls):
        if cls._pool is None:
            cls.init_pool()
        return cls._pool.get_connection()

    @classmethod
    def return_connection(cls, connection):
        """Método para devolver conexión al pool"""
        if connection:
            connection.close()