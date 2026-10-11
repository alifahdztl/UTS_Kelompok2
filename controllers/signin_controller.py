from tkinter import messagebox
from models.signin_model import SigninModel

class SigninController:
    def __init__(self):
        self.model = SigninModel()

    def registrasi_pelanggan(self, nama, email, telepon):
        """
        Memproses validasi dan registrasi pelanggan baru melalui SigninModel.
        Mengembalikan True jika berhasil, atau False jika gagal.
        """
        # Validasi field kosong
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Nama, Email, dan Nomor Telepon wajib diisi!")
            return False

        # Panggil Model untuk menyimpan data ke database
        berhasil = self.model.insert_pelanggan(nama, telepon, email)

        if berhasil:
            messagebox.showinfo("Sukses", "Registrasi Berhasil!\nSilakan login menggunakan data Anda.")
            return True
        else:
            messagebox.showerror("Error", "Gagal melakukan registrasi atau terjadi kesalahan database.")
            return False