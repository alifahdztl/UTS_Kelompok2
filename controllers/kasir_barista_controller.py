from models.kasir_barista_model import KasirBaristaModel
from tkinter import messagebox

class KasirBaristaController:
    def __init__(self):
        self.model = KasirBaristaModel()

    def verifikasi_login(self, nama, email, telepon):
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return None
        
        user = self.model.login_kasir(nama, email, telepon)
        if user:
            return user
        else:
            messagebox.showerror("Error", "Data kasir/barista tidak ditemukan di database!")
            return None

    def registrasi_kasir(self, nama, email, telepon):
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom harus diisi!")
            return False

        try:
            success = self.model.registrasi_kasir(nama, email, telepon)
            if success:
                messagebox.showinfo("Sukses", "Registrasi kasir/barista berhasil! Silakan login.")
                return True
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")
        return False