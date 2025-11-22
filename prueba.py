import mysql.connector

try:
    conn = mysql.connector.connect(
        host='instancia-iot-rds.cja06eu6ednb.us-east-1.rds.amazonaws.com',
        port=3306,
        user='admin',  # ← CAMBIA POR TU USUARIO REAL
        password='Admin12345#!',  # ← CAMBIA POR TU PASSWORD REAL
        connection_timeout=10
    )
    print("✅ ¡Conexión exitosa a RDS!")

    # Si funciona, prueba crear/ver una base de datos
    cursor = conn.cursor()
    cursor.execute("SHOW DATABASES;")
    databases = cursor.fetchall()
    print("📁 Bases de datos disponibles:")
    for db in databases:
        print(f" - {db[0]}")

    cursor.close()
    conn.close()

except mysql.connector.Error as e:
    print(f"❌ Error de MySQL: {e}")
except Exception as e:
    print(f"❌ Error general: {e}")