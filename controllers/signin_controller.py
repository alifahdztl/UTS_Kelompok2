from tkinter import messagebox
from config.database import Database

class SigninController:
    def __init__(self):
        self.db = Database()

    def registrasi_pelanggan(self, nama, email, telepon):
        """
        Memproses validasi dan penyimpanan data pelanggan baru ke database MySQL.
        Mengembalikan True jika berhasil, atau False jika gagal.
        """
        # Validasi field kosong
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Nama, Email, dan Nomor Telepon wajib diisi!")
            return False

        conn = self.db.get_connection()
        if not conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            query = "INSERT INTO pelanggan (nama_pelanggan, nomor_telepon, email) VALUES (%s, %s, %s)"
            cursor.execute(query, (nama, telepon, email))
            conn.commit()

            messagebox.showinfo("Sukses", "Registrasi Berhasil!\nSilakan login menggunakan data Anda.")
            return True

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Error", f"Terjadi kesalahan database: {e}")
            return False

        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()