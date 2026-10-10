from config.database import Database

class PembayaranModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "pembayaran"

    def get_all_pembayaran(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_pembayaran(self, id_pesanan, metode_pembayaran, jumlah_bayar, status_pembayaran):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (id_pesanan, metode_pembayaran, jumlah_bayar, status_pembayaran) VALUES (%s, %s, %s, %s)"
            val = (id_pesanan, metode_pembayaran, jumlah_bayar, status_pembayaran)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False