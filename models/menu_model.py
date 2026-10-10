from config.database import Database

class MenuModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "menu"

    def get_all_menu(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_menu(self, nama_menu, kategori, harga, stok, status_menu):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama_menu, kategori, harga, stok, status_menu) VALUES (%s, %s, %s, %s, %s)"
            val = (nama_menu, kategori, harga, stok, status_menu)
            cursor.execute(query, val)
            self.conn.commit()
            cursor.close()
            return True
        return False