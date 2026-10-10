import sys
import os

# Menambahkan direktori root proyek agar import modul berhasil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")


class SigninPelangganView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Warm Coffee - Sign In Pelanggan")
        self.geometry("450x580")
        self.resizable(False, False)
        self.configure(fg_color="#231915")

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#362822")
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(
            self.main_frame, text="SIGN IN PELANGGAN", font=ctk.CTkFont(size=22, weight="bold"), text_color="#F5E6D3"
        )
        self.label_title.pack(pady=(30, 5))

        self.label_subtitle = ctk.CTkLabel(
            self.main_frame, text="Daftarkan akun member Warm Coffee Anda", font=ctk.CTkFont(size=12), text_color="#A68A78"
        )
        self.label_subtitle.pack(pady=(0, 20))

        entry_kwargs = {
            "master": self.main_frame, "width": 300, "height": 40, "fg_color": "#231915",
            "border_color": "#8E5A2A", "border_width": 1, "text_color": "#F5E6D3", "placeholder_text_color": "#A68A78"
        }

        self.entry_nama = ctk.CTkEntry(placeholder_text="Nama Pelanggan", **entry_kwargs)
        self.entry_nama.pack(pady=8)

        self.entry_email = ctk.CTkEntry(placeholder_text="Email", **entry_kwargs)
        self.entry_email.pack(pady=8)

        self.entry_telepon = ctk.CTkEntry(placeholder_text="Nomor Telepon", **entry_kwargs)
        self.entry_telepon.pack(pady=8)

        self.btn_signin = ctk.CTkButton(
            self.main_frame, text="DAFTAR", font=ctk.CTkFont(size=13, weight="bold"),
            width=300, height=40, fg_color="#965829", hover_color="#7A451E", text_color="#FFFFFF", command=self.proses_signin
        )
        self.btn_signin.pack(pady=(25, 10))

        self.btn_kembali = ctk.CTkButton(
            self.main_frame, text="Kembali ke Login", font=ctk.CTkFont(size=11),
            width=300, height=30, fg_color="transparent", hover_color="#231915", text_color="#F5E6D3", command=self.buka_login
        )
        self.btn_kembali.pack(pady=5)

    def proses_signin(self):
        """Hanya mengambil input lokal tanpa controller dan tanpa database"""
        nama = self.entry_nama.get().strip()
        email = self.entry_email.get().strip()
        telepon = self.entry_telepon.get().strip()

        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Nama, Email, dan Nomor Telepon wajib diisi!")
            return

        # Pesan simulasi lokal (tidak menyimpan ke database)
        messagebox.showinfo("Informasi", f"Registrasi simulasi berhasil untuk: {nama}\n(Tidak terhubung ke controller/database)")
        self.buka_login()

    def buka_login(self):
        """Menutup jendela sign in dan membuka kembali jendela login statis"""
        self.destroy()
        from views.login_view import LoginView
        app_login = LoginView()
        app_login.mainloop()


if __name__ == "__main__":
    app = SigninPelangganView()
    app.mainloop()