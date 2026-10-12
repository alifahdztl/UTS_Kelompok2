import sys
import os
import importlib.util

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox
from controllers.kasir_barista_controller import KasirBaristaController

ctk.set_appearance_mode("Dark")

class LoginKasirBaristaView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.controller = KasirBaristaController()

        self.title("Warm Coffee - Login Kasir & Barista")
        self.geometry("500x620")
        self.resizable(False, False)
        self.configure(fg_color="#1e1411")

        self.main_frame = ctk.CTkFrame(self, fg_color="#2b1f1a", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="LOGIN KASIR & BARISTA", 
            font=ctk.CTkFont(size=22, weight="bold"), 
            text_color="#F5E6D3"
        )
        self.title_label.pack(pady=(45, 8))

        self.subtitle_label = ctk.CTkLabel(
            self.main_frame, 
            text="Masukkan data akun staf Warm Coffee", 
            font=ctk.CTkFont(size=14), 
            text_color="#D2B48C"
        )
        self.subtitle_label.pack(pady=(0, 35))

        entry_kwargs = {
            "master": self.main_frame,
            "width": 360,
            "height": 45,
            "fg_color": "#1e1411",
            "border_color": "#8E5A2A",
            "border_width": 2,
            "text_color": "#F5E6D3",
            "placeholder_text_color": "#A89F91",
            "font": ctk.CTkFont(size=13)
        }

        self.entry_nama = ctk.CTkEntry(placeholder_text="Nama Kasir / Barista", **entry_kwargs)
        self.entry_nama.pack(pady=10)

        self.entry_email = ctk.CTkEntry(placeholder_text="Email", **entry_kwargs)
        self.entry_email.pack(pady=10)

        self.entry_telepon = ctk.CTkEntry(placeholder_text="Nomor Telepon", show="*", **entry_kwargs)
        self.entry_telepon.pack(pady=(10, 30))

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
        self.btn_login.pack(pady=(0, 15))

        self.btn_to_signin = ctk.CTkButton(
            self.main_frame,
            text="Belum punya akun? Sign In",
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            hover_color="#2b1f1a",
            text_color="#F5E6D3",
            command=self.buka_signin
        )
        self.btn_to_signin.pack(pady=5)

    def handle_login(self):
        nama = self.entry_nama.get().strip()
        email = self.entry_email.get().strip()
        telepon = self.entry_telepon.get().strip()

        if not nama or not email or not telepon:
            messagebox.showwarning("Peringatan", "Semua kolom data staf harus diisi!")
            return

        user = self.controller.verifikasi_login(nama, email, telepon)

        if user:
            messagebox.showinfo("Sukses", f"Selamat datang, {user.get('nama_kasir', nama)}!")
            
            # 1. Tutup jendela login
            self.destroy()
            
            # 2. Buka halaman orderstatus_kasir_barista_view.py secara langsung dan mulus
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'orderstatus_kasir_barista_view.py'))
            spec = importlib.util.spec_from_file_location("orderstatus_kasir_barista_view", file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            app_kasir = module.KasirOrderStatusView()
            app_kasir.mainloop()

    def buka_signin(self):
        self.destroy()
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'signin_kasir_barista.py'))
        spec = importlib.util.spec_from_file_location("signin_kasir_barista", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        app_signin = module.KasirBaristaSigninView()
        app_signin.mainloop()


if __name__ == "__main__":
    app = LoginKasirBaristaView()
    app.mainloop()