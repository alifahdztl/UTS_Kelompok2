from config.database import Database

class LoginModel:
    def __init__(self):
        self.db = Database()

    def get_pelanggan_by_credentials(self, nama, email, telepon):
        """
        Mengambil data pelanggan dari database berdasarkan nama, email, dan nomor telepon.
        Mengembalikan dictionary data pelanggan jika ditemukan, atau None jika tidak ada.
        """
        conn = self.db.get_connection()
        if not conn:
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM pelanggan WHERE nama_pelanggan = %s AND email = %s AND nomor_telepon = %s"
            cursor.execute(query, (nama, email, telepon))
            pelanggan = cursor.fetchone()

            cursor.close()
            conn.close()
            return pelanggan

        except Exception as e:
            print(f"Error database pada LoginModel: {e}")
            return None