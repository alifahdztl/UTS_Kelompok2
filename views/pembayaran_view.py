import sys
import os

# Menambahkan direktori root proyek agar import modul berhasil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import messagebox

ctk.set_appearance_mode("Dark")


class PembayaranView(ctk.CTk):
    def __init__(self, order_data=None, pelanggan_data=None):
        super().__init__()

        # Data dikosongkan secara default jika tidak dikirim dari halaman sebelumnya
        self.order_data = order_data or {}
        self.pelanggan_data = pelanggan_data or {}

        # Konfigurasi Window Pembayaran
        self.title("Warm Coffee - Halaman Pembayaran")
        self.geometry("550x540")
        self.resizable(False, False)
        self.configure(fg_color="#231915")

        # Container Utama
        self.main_card = ctk.CTkFrame(self, fg_color="#362822", corner_radius=15)
        self.main_card.pack(pady=20, padx=20, fill="both", expand=True)

        # Header Title
        self.lbl_title = ctk.CTkLabel(
            self.main_card,
            text="KONFIRMASI PEMBAYARAN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F5E6D3"
        )
        self.lbl_title.pack(pady=(25, 15))

        # Mengambil data secara dinamis (jika kosong, tampilkan tanda '-')
        nama = self.pelanggan_data.get("nama_pelanggan", "-")
        if nama != "-":
            nama = nama.title()
            
        no_antrian = self.order_data.get("nomor_antrian", "-")
        total_harga = self.order_data.get("total_harga", 0)

        # Detail Ringkasan Pembayaran
        self.lbl_detail = ctk.CTkLabel(
            self.main_card,
            text=f"Nama Pelanggan : {nama}\nNo. Antrian        : {no_antrian}\nTotal Tagihan    : Rp {total_harga:,.0f}",
            font=ctk.CTkFont(size=14),
            text_color="#F5E6D3",
            justify="left"
        )
        self.lbl_detail.pack(pady=10, padx=40, anchor="w")

        # Kotak Keterangan Status Lunas
        self.status_frame = ctk.CTkFrame(self.main_card, fg_color="#1e1411", corner_radius=10, border_color="#8E5A2A", border_width=2)
        self.status_frame.pack(fill="x", padx=40, pady=15)

        self.lbl_status_lunas = ctk.CTkLabel(
            self.status_frame,
            text="STATUS: LUNAS\n(Pembayaran Berhasil Dikonfirmasi)",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#2ECC71"
        )
        self.lbl_status_lunas.pack(pady=20, padx=20)

        # Tombol Proses & Konfirmasi Pembayaran Lokal
        self.btn_bayar = ctk.CTkButton(
            self.main_card,
            text="KONFIRMASI & BAYAR SEKARANG",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            height=40,
            command=self.eksekusi_pembayaran
        )
        self.btn_bayar.pack(pady=(10, 5), padx=40, fill="x")

        # Tombol Selesai / Kembali
        self.btn_selesai = ctk.CTkButton(
            self.main_card,
            text="KEMBALI / TUTUP",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#965829",
            hover_color="#7A451E",
            height=38,
            command=self.destroy
        )
        self.btn_selesai.pack(pady=(5, 25), padx=40, fill="x")

    def eksekusi_pembayaran(self):
        """Memproses pembayaran secara lokal tanpa controller/database"""
        messagebox.showinfo("Sukses", "Pembayaran berhasil dikonfirmasi secara lokal! (Status: Lunas)")
        self.destroy()


if __name__ == "__main__":
    # Dikosongkan saat dijalankan mandiri tanpa parameter
    app = PembayaranView()
    app.mainloop()