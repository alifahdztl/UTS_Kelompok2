import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from controllers.kasir_barista_controller import KasirBaristaController

ctk.set_appearance_mode("Dark")

class KasirBaristaSigninView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.controller = KasirBaristaController()

        self.title("Warm Coffee - Sign In Kasir & Barista")
        self.geometry("450x580")
        self.resizable(False, False)
        self.configure(fg_color="#231915")

        self.main_frame = ctk.CTkFrame(self, corner_radius=20, fg_color="#362822")
        self.main_frame.pack(pady=30, padx=30, fill="both", expand=True)

        self.label_title = ctk.CTkLabel(
            self.main_frame, text="SIGN IN KASIR & BARISTA", font=ctk.CTkFont(size=20, weight="bold"), text_color="#F5E6D3"
        )
        self.label_title.pack(pady=(30, 5))

        self.label_subtitle = ctk.CTkLabel(
            self.main_frame, text="Daftarkan akun staf baru Warm Coffee", font=ctk.CTkFont(size=12), text_color="#A68A78"
        )
        self.label_subtitle.pack(pady=(0, 20))

        entry_kwargs = {
            "master": self.main_frame, "width": 300, "height": 40, "fg_color": "#231915",
            "border_color": "#8E5A2A", "border_width": 1, "text_color": "#F5E6D3", "placeholder_text_color": "#A68A78"
        }

        self.entry_nama = ctk.CTkEntry(placeholder_text="Nama Kasir / Barista", **entry_kwargs)
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
        nama = self.entry_nama.get().strip()
        email = self.entry_email.get().strip()
        telepon = self.entry_telepon.get().strip()

        sukses = self.controller.registrasi_kasir(nama, email, telepon)
        if sukses:
            self.buka_login()

    def buka_login(self):
        self.destroy()
        # Menggunakan import dinamis agar bersih dari peringatan circular Pylance di top-level
        import importlib.util
        file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'login_kasir_barista_view.py'))
        spec = importlib.util.spec_from_file_location("login_kasir_barista_view", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        app_login = module.LoginKasirBaristaView()
        app_login.mainloop()


if __name__ == "__main__":
    app = KasirBaristaSigninView()
    app.mainloop()