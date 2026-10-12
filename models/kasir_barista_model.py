from config.database import Database

class KasirBaristaModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "kasir_barista"

    def login_kasir(self, nama, email, telepon):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name} WHERE nama_kasir = %s AND email = %s AND nomor_telepon = %s"
            cursor.execute(query, (nama, email, telepon))
            result = cursor.fetchone()
            cursor.close()
            return result
        return None

    def registrasi_kasir(self, nama_kasir, email, nomor_telepon):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama_kasir, nomor_telepon, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (nama_kasir, nomor_telepon, email))
            self.conn.commit()
            cursor.close()
            return True
        return False