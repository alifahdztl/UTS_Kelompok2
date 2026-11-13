from config.database import Database
from config.security import hash_password


class LoginModel:
    def __init__(self):
        self.db = Database()

    @staticmethod
    def hash_password(password):
        return hash_password(password)

    def get_pelanggan_by_credentials(self, nama, email, password):
        """
        Autentikasi pelanggan: nama + email + HASH password harus cocok dengan data di database.
        Mengembalikan dictionary data pelanggan (tanpa password) jika cocok, atau None jika tidak.
        """
        conn = self.db.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = (
                "SELECT id_pelanggan, nama_pelanggan, nomor_telepon, email FROM pelanggan "
                "WHERE nama_pelanggan = %s AND email = %s AND password = %s"
            )
            cursor.execute(query, (nama, email, self.hash_password(password)))
            pelanggan = cursor.fetchone()

            cursor.close()
            conn.close()
            return pelanggan

        except Exception as e:
            print(f"Error database pada LoginModel: {e}")
            return None
