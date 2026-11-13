import sys
import os

# Menambahkan direktori root proyek ke sistem path agar modul 'config' terbaca
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.database import Database
from config.security import hash_password


class KasirBaristaModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "kasir_barista"

    @staticmethod
    def hash_password(password):
        return hash_password(password)

    def get_all_kasir(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT nama_kasir, nomor_telepon, email FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def login_kasir(self, nama, email, password):
        """Autentikasi: bandingkan HASH password input dengan hash di database (parameterized query)."""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = (
                f"SELECT nama_kasir, email, nomor_telepon FROM {self.table_name} "
                "WHERE nama_kasir = %s AND email = %s AND password = %s"
            )
            cursor.execute(query, (nama, email, self.hash_password(password)))
            result = cursor.fetchone()
            cursor.close()
            return result
        return None

    def registrasi_kasir(self, nama_kasir, email, nomor_telepon, password):
        """Menyimpan akun baru; password otomatis di-hash SHA-256 sebelum masuk database."""
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (nama_kasir, nomor_telepon, email, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nama_kasir, nomor_telepon, email, self.hash_password(password)))
            self.conn.commit()
            cursor.close()
            return True
        return False

    def get_all_kasir(self):
        """Mengambil seluruh data kasir dan barista dari database"""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []
