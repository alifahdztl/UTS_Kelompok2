import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from views.logo_helper import pasang_logo, pasang_ikon

ctk.set_appearance_mode("Dark")


class WelcomeView(ctk.CTk):
    """Halaman awal: memilih masuk sebagai Pelanggan atau Kasir & Barista."""

    def __init__(self):
        super().__init__()

        self.title("Kopiloka")
        self.geometry("500x460")
        self.resizable(False, False)
        self.configure(fg_color="#1e1411")
        pasang_ikon(self)

        self.main_frame = ctk.CTkFrame(self, fg_color="#2b1f1a", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        # Logo (sudah memuat nama "KOPILOKA" dan tulisan "PEMESANAN CAFE")
        if pasang_logo(self.main_frame, skala=2, pady=(30, 20)) is None:
            # cadangan jika file logo tidak ditemukan
            ctk.CTkLabel(
                self.main_frame, text="KOPILOKA",
                font=ctk.CTkFont(size=26, weight="bold"), text_color="#F5E6D3"
            ).pack(pady=(45, 35))

        self.btn_pelanggan = ctk.CTkButton(
            self.main_frame, text="MASUK SEBAGAI PELANGGAN",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#965829", hover_color="#7A451E", height=45, width=320
        )
        self.btn_pelanggan.pack(pady=10)

        self.btn_kasir = ctk.CTkButton(
            self.main_frame, text="MASUK SEBAGAI KASIR & BARISTA",
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#8E5A2A", hover_color="#7A451E", height=45, width=320
        )
        self.btn_kasir.pack(pady=10)


if __name__ == "__main__":
    app = WelcomeView()
    app.mainloop()