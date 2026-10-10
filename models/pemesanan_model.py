from config.database import Database

class PemesananModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "pemesanan"

    def get_all_pemesanan(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_pemesanan(self, id_pelanggan, nomor_antrian, total_harga, status_pesanan):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (id_pelanggan, nomor_antrian, total_harga, status_pesanan) VALUES (%s, %s, %s, %s)"
            val = (id_pelanggan, nomor_antrian, total_harga, status_pesanan)
            cursor.execute(query, val)
            self.conn.commit()
            id_pesanan = cursor.lastrowid
            cursor.close()
            return id_pesanan
        return None