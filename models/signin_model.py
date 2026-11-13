from config.database import Database
from config.security import hash_password


class SigninModel:
    def __init__(self):
        self.db = Database()

    @staticmethod
    def hash_password(password):
        return hash_password(password)

    def insert_pelanggan(self, nama, telepon, email, password):
        """
        Menyimpan data pelanggan baru ke tabel pelanggan.
        Password otomatis di-hash SHA-256 sebelum disimpan.
        Mengembalikan True jika berhasil, atau False jika gagal.
        """
        conn = self.db.get_connection()
        if not conn:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO pelanggan (nama_pelanggan, nomor_telepon, email, password) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (nama, telepon, email, self.hash_password(password)))
            conn.commit()
            return True

        except Exception as e:
            if conn:
                conn.rollback()
            print(f"Error database pada SigninModel: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
