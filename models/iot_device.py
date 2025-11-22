from database import Database


class IotDeviceModel:
    """Métodos que envuelven a los Stored Procedures."""

    @staticmethod
    def select_all():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('sp_iot_devices_select_all')
            rows = []
            for result in cursor.stored_results():
                rows = result.fetchall()
            return rows
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def select_last5():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('sp_iot_devices_select_last5')
            rows = []
            for result in cursor.stored_results():
                rows = result.fetchall()
            return rows
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def get_last_status_texto():
        conn = Database.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.callproc('sp_iot_devices_last_status_texto')
            value = None
            for result in cursor.stored_results():
                row = result.fetchone()
                if row:
                    value = row.get('status_texto')
            return value
        finally:
            cursor.close()
            conn.close()

            def insert(name: str, ip: str, status_clave: int, status_texto: str):
                conn = Database.get_connection()
                cursor = conn.cursor(dictionary=True)
                try:
                    cursor.callproc('sp_iot_devices_insert', (name, ip, status_clave, status_texto))
                    new_id = None
                    for result in cursor.stored_results():
                        row = result.fetchone()
                        if row:
                            # el SP retorna SELECT LAST_INSERT_ID() AS new_id;
                            new_id = row.get('new_id') or list(row.values())[0]
                    conn.commit()
                    return new_id
                finally:
                    cursor.close()
                    conn.close()