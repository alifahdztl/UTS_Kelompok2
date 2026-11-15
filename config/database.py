import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.db_name = "database_sistem_informasi_pemesanan_coffe_shop"  # Sesuai dengan database Anda[cite: 6]
        self.username = "root"
        self.password = ""
        self.conn = None

    def get_connection(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                database=self.db_name,
                user=self.username,
                password=self.password,
                autocommit=True,  # tiap query membaca data terbaru; transaksi manual memakai start_transaction()[cite: 6]
                use_pure=True     # <-- TAMBAHKAN BARIS INI (Wajib untuk file .exe)
            )
            if self.conn.is_connected():
                return self.conn
        except Error as e:
            print(f"Koneksi Gagal: {e}")
            return None