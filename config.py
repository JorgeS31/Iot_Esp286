import os

class Config:
    # Variables de entorno con valores por default
    DB_HOST = os.environ.get("DB_HOST", "instancia-iot-rds.cja06eu6ednb.us-east-1.rds.amazonaws.com")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))
    DB_NAME = os.environ.get("DB_NAME", "iot_db")
    DB_USER = os.environ.get("DB_USER", "admin")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "Admin12345#!")
    POOL_NAME = os.environ.get("POOL_NAME", "iot_pool")
    POOL_SIZE = int(os.environ.get("POOL_SIZE", 5))
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "*")

    # Config pool MySQL
    DB_CONFIG = {
        "host": DB_HOST,
        "port": DB_PORT,
        "database": DB_NAME,
        "user": DB_USER,
        "password": DB_PASSWORD,
        "autocommit": True,
    }