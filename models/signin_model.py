from config.database import Database

class SigninModel:
    def __init__(self):
        self.db = Database()

    def insert_pelanggan(self, nama, telepon, email):
        """
        Menyimpan data pelanggan baru ke dalam tabel pelanggan.
        Mengembalikan True jika berhasil, atau False jika gagal.
        """
        conn = self.db.get_connection()
        if not conn:
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO pelanggan (nama_pelanggan, nomor_telepon, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (nama, telepon, email))
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