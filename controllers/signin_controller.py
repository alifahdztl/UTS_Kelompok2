from tkinter import messagebox
from models.signin_model import SigninModel

PANJANG_MINIMAL_PASSWORD = 6


class SigninController:
    def __init__(self):
        self.model = SigninModel()

    def registrasi_pelanggan(self, nama, email, telepon, password):
        """
        Memproses validasi dan registrasi pelanggan baru melalui SigninModel.
        Mengembalikan True jika berhasil, atau False jika gagal.
        """
        if not nama or not email or not telepon or not password:
            messagebox.showwarning("Peringatan", "Nama, Email, Nomor Telepon, dan Password wajib diisi!")
            return False

        if len(password) < PANJANG_MINIMAL_PASSWORD:
            messagebox.showwarning("Peringatan", f"Password minimal {PANJANG_MINIMAL_PASSWORD} karakter!")
            return False

        berhasil = self.model.insert_pelanggan(nama, telepon, email, password)

        if berhasil:
            messagebox.showinfo("Sukses", "Registrasi Berhasil!\nSilakan login menggunakan data Anda.")
            return True

        messagebox.showerror("Error", "Gagal melakukan registrasi atau terjadi kesalahan database.")
        return False
