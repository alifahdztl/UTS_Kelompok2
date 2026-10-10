from tkinter import messagebox
from config.database import Database

class LoginController:
    def __init__(self):
        self.db = Database()

    def verifikasi_login(self, nama, email, telepon):
        """
        Memproses validasi dan autentikasi login pelanggan berdasarkan database.
        Mengembalikan data pelanggan (dict) jika berhasil, atau False/None jika gagal.
        """
        # Validasi field kosong
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Nama, Email, dan Nomor Telepon wajib diisi!")
            return None

        conn = self.db.get_connection()
        if not conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return None

        try:
            cursor = conn.cursor(dictionary=True)
            query = "SELECT * FROM pelanggan WHERE nama_pelanggan = %s AND email = %s AND nomor_telepon = %s"
            cursor.execute(query, (nama, email, telepon))
            pelanggan = cursor.fetchone()

            cursor.close()
            conn.close()

            if pelanggan:
                messagebox.showinfo("Sukses", f"Login Berhasil!\nSelamat datang, {pelanggan['nama_pelanggan']}.")
                return pelanggan
            else:
                messagebox.showerror("Akses Ditolak", "Data tidak cocok! Hanya pelanggan terdaftar yang bisa masuk.")
                return None

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan database: {e}")
            return None