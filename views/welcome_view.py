import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk

ctk.set_appearance_mode("Dark")


class WelcomeView(ctk.CTk):
    """Halaman awal: memilih masuk sebagai Pelanggan atau Kasir & Barista."""

    def __init__(self):
        super().__init__()

        self.title("Warm Coffee")
        self.geometry("500x420")
        self.resizable(False, False)
        self.configure(fg_color="#1e1411")

        self.main_frame = ctk.CTkFrame(self, fg_color="#2b1f1a", corner_radius=20)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=30)

        ctk.CTkLabel(
            self.main_frame, text="WARM COFFEE",
            font=ctk.CTkFont(size=26, weight="bold"), text_color="#F5E6D3"
        ).pack(pady=(45, 8))

        ctk.CTkLabel(
            self.main_frame, text="Sistem Informasi Pemesanan Coffee Shop",
            font=ctk.CTkFont(size=13), text_color="#D2B48C"
        ).pack(pady=(0, 35))

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
