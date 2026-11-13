from config.database import Database

class DetailPesananModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "detail_pesanan"

    def get_all_detail_pesanan(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_detail_pesanan(self, id_pesanan, id_menu, jumlah, subtotal):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (id_pesanan, id_menu, jumlah, subtotal) VALUES (%s, %s, %s, %s)"
            val = (id_pesanan, id_menu, jumlah, subtotal)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False

    def get_by_pesanan(self, id_pesanan):
        """Daftar menu yang dipesan pada satu pesanan (nama_menu, qty)."""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"""
                SELECT m.nama_menu, dp.jumlah AS qty
                FROM {self.table_name} dp
                JOIN menu m ON dp.id_menu = m.id_menu
                WHERE dp.id_pesanan = %s
            """
            cursor.execute(query, (id_pesanan,))
            result = cursor.fetchall()
            cursor.close()
            return result
        return []
