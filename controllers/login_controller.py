from tkinter import messagebox
from models.login_model import LoginModel


class LoginController:
    def __init__(self):
        self.model = LoginModel()

    def verifikasi_login(self, nama, email, password):
        """
        Memproses validasi dan autentikasi login pelanggan.
        Mengembalikan data pelanggan jika berhasil, atau None jika gagal.
        """
        if not nama or not email or not password:
            messagebox.showwarning("Peringatan", "Nama, Email, dan Password wajib diisi!")
            return None

        pelanggan = self.model.get_pelanggan_by_credentials(nama, email, password)

        if pelanggan:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {pelanggan['nama_pelanggan']}.")
            return pelanggan

        messagebox.showerror("Login Gagal", "Nama, email, atau password salah, atau gagal terhubung ke database!")
        return None
