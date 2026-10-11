from tkinter import messagebox
from models.login_model import LoginModel

class LoginController:
    def __init__(self):
        self.model = LoginModel()

    def verifikasi_login(self, nama, email, telepon):
        """
        Memproses validasi dan autentikasi login pelanggan.
        """
        # Validasi field kosong
        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Nama, Email, dan Nomor Telepon wajib diisi!")
            return None

        # Memanggil Model untuk mengambil data dari database
        pelanggan = self.model.get_pelanggan_by_credentials(nama, email, telepon)

        # Cek koneksi atau error dari model
        # (Jika conn gagal, model mengembalikan None. Kita bisa handle atau cek terpisah jika ingin pesan error khusus koneksi)
        
        if pelanggan:
            messagebox.showinfo("Sukses", f"Login Berhasil!\nSelamat datang, {pelanggan['nama_pelanggan']}.")
            return pelanggan
        else:
            # Jika pelanggan bernilai None (bisa karena salah data atau database error)
            messagebox.showerror("Akses Ditolak", "Data tidak cocok atau gagal terhubung ke database! Hanya pelanggan terdaftar yang bisa masuk.")
            return None