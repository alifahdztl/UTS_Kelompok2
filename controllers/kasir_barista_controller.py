from tkinter import messagebox
from models.kasir_barista_model import KasirBaristaModel

PANJANG_MINIMAL_PASSWORD = 6


class KasirBaristaController:
    def __init__(self):
        self.model = KasirBaristaModel()

    def verifikasi_login(self, nama, email, password):
        if not nama or not email or not password:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return None

        user = self.model.login_kasir(nama, email, password)
        if user:
            messagebox.showinfo("Login Berhasil", f"Selamat datang, {user['nama_kasir']}.")
            return user

        messagebox.showerror("Login Gagal", "Nama, email, atau password salah!")
        return None

    def registrasi_kasir(self, nama, email, telepon, password):
        if not nama or not email or not telepon or not password:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return False

        if len(password) < PANJANG_MINIMAL_PASSWORD:
            messagebox.showwarning("Peringatan", f"Password minimal {PANJANG_MINIMAL_PASSWORD} karakter!")
            return False

        try:
            success = self.model.registrasi_kasir(nama, email, telepon, password)
            if success:
                messagebox.showinfo("Sukses", "Registrasi kasir/barista berhasil! Silakan login.")
                return True
            messagebox.showerror("Error", "Gagal terhubung ke database!")
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        return False
