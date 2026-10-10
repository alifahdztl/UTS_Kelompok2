from config.database import Database

class PelangganModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "pelanggan"

    def get_all_pelanggan(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_pelanggan(self, nama_pelanggan, nomor_telepon, email):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama_pelanggan, nomor_telepon, email) VALUES (%s, %s, %s)"
            val = (nama_pelanggan, nomor_telepon, email)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False