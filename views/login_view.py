import sys
import os

# Menambahkan direktori root proyek agar import modul berhasil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")


class LoginView(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Konfigurasi Window Login
        self.title("Warm Coffee - Login Pelanggan")
        self.geometry("500x620")
        self.resizable(False, False)
        self.configure(fg_color="#1e1411")

        # Container Utama (Kotak Panel Besar di Tengah)
        self.main_frame = ctk.CTkFrame(self, fg_color="#2b1f1a", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Header / Judul
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="LOGIN PELANGGAN", 
            font=ctk.CTkFont(size=24, weight="bold"), 
            text_color="#F5E6D3"
        )
        self.title_label.pack(pady=(45, 8))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, 
            text="Masukkan data member Warm Coffee Anda", 
            font=ctk.CTkFont(size=14), 
            text_color="#D2B48C"
        )
        self.subtitle_label.pack(pady=(0, 35))

        # Input Nama Pelanggan
        self.entry_nama = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Nama Pelanggan", 
            width=360, 
            height=45,
            fg_color="#1e1411", 
            border_color="#8E5A2A", 
            border_width=2,
            text_color="#F5E6D3",
            placeholder_text_color="#A89F91",
            font=ctk.CTkFont(size=13)
        )
        self.entry_nama.pack(pady=10)

        # Input Email
        self.entry_email = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Email", 
            width=360, 
            height=45,
            fg_color="#1e1411", 
            border_color="#8E5A2A", 
            border_width=2,
            text_color="#F5E6D3",
            placeholder_text_color="#A89F91",
            font=ctk.CTkFont(size=13)
        )
        self.entry_email.pack(pady=10)

        # Input Nomor Telepon (Dengan bintang-bintang `show="*"`)
        self.entry_telepon = ctk.CTkEntry(
            self.main_frame, 
            placeholder_text="Nomor Telepon", 
            width=360, 
            height=45,
            fg_color="#1e1411", 
            border_color="#8E5A2A", 
            border_width=2,
            text_color="#F5E6D3",
            placeholder_text_color="#A89F91",
            font=ctk.CTkFont(size=13),
            show="*"
        )
        self.entry_telepon.pack(pady=(10, 30))

        # Tombol Masuk
        self.btn_login = ctk.CTkButton(
            self.main_frame, 
            text="MASUK", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#965829", 
            hover_color="#7A451E", 
            height=45, 
            width=360,
            command=self.handle_login
        )
        self.btn_login.pack(pady=(0, 20))

    def handle_login(self):
        """Hanya mengambil input lokal tanpa controller dan tanpa database"""
        nama = self.entry_nama.get().strip()
        email = self.entry_email.get().strip()
        telepon = self.entry_telepon.get().strip()

        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom wajib diisi!")
            return

        # Pesan dummy saat tombol diklik
        messagebox.showinf("Informasi", f"Tombol Masuk diklik oleh: {nama}\n(Tampilan mandiri tanpa controller/database)")


if __name__ == "__main__":
    app = LoginView()
    app.mainloop()