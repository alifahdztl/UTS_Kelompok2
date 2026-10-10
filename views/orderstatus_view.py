import sys
import os

# Menambahkan direktori root proyek agar import modul berhasil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox

ctk.set_appearance_mode("Dark")


class OrderStatusView(ctk.CTk):
    def __init__(self, order_data=None, pelanggan_data=None):
        super().__init__()

        self.order_data = order_data or {}
        self.pelanggan_data = pelanggan_data or {"nama_pelanggan": "Pelanggan"}

        # Konfigurasi Window Informasi Pesanan
        self.title("Warm Coffee - Informasi Pesanan")
        self.geometry("820x480")
        self.resizable(False, False)
        self.configure(fg_color="#231915")

        # Container Utama
        self.main_card = ctk.CTkFrame(self, fg_color="#362822", corner_radius=15)
        self.main_card.pack(pady=20, padx=20, fill="both", expand=True)

        # Title Header
        self.lbl_title = ctk.CTkLabel(
            self.main_card,
            text="INFORMASI & UBAH STATUS PESANAN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F5E6D3"
        )
        self.lbl_title.pack(pady=(20, 15))

        # Style Custom untuk Treeview Ringkasan
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Status.Treeview",
            background="#231915",
            foreground="#F5E6D3",
            rowheight=32,
            fieldbackground="#231915"
        )
        style.configure(
            "Status.Treeview.Heading",
            background="#8E5A2A",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold")
        )

        # Tabel Informasi Pesanan
        columns = ("no_antrian", "nama_pelanggan", "menu_dipesan", "status_pesanan")
        self.tree_info = ttk.Treeview(
            self.main_card,
            columns=columns,
            show="headings",
            height=4,
            style="Status.Treeview"
        )

        self.tree_info.heading("no_antrian", text="No. Antrian")
        self.tree_info.heading("nama_pelanggan", text="Nama Pelanggan")
        self.tree_info.heading("menu_dipesan", text="Menu Dipesan")
        self.tree_info.heading("status_pesanan", text="Status Pesanan")

        self.tree_info.column("no_antrian", width=110, anchor="center")
        self.tree_info.column("nama_pelanggan", width=160, anchor="w")
        self.tree_info.column("menu_dipesan", width=340, anchor="w")
        self.tree_info.column("status_pesanan", width=130, anchor="center")

        self.tree_info.pack(fill="both", expand=True, padx=20, pady=10)

        # Format daftar menu yang dipesan dari keranjang
        menu_items = self.order_data.get("items", [])
        menu_text_list = [f"{item['nama_menu']} ({item['qty']}x)" for item in menu_items]
        daftar_menu_str = ", ".join(menu_text_list) if menu_text_list else "-"

        # Ambil status awal pesanan
        self.current_status = self.order_data.get("status_pesanan", "Pending")

        # Memasukkan data ke tabel
        self.tree_info.insert("", "end", iid="row_1", values=(
            self.order_data.get("nomor_antrian", "A-001"),
            self.pelanggan_data.get("nama_pelanggan", "Pelanggan").title(),
            daftar_menu_str,
            self.current_status
        ))

        # ----------------- PANEL UBAH STATUS PESANAN -----------------
        self.update_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.update_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_select_status = ctk.CTkLabel(
            self.update_frame,
            text="Ubah Status Pesanan:",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#F5E6D3"
        )
        self.lbl_select_status.pack(side="left", padx=(0, 10))

        # Dropdown pilihan status (Pending, Diproses, Selesai)
        self.combo_status = ctk.CTkOptionMenu(
            self.update_frame,
            values=["Pending", "Diproses", "Selesai"],
            fg_color="#231915",
            button_color="#8E5A2A",
            button_hover_color="#7A451E",
            text_color="#F5E6D3",
            width=150
        )
        self.combo_status.set(self.current_status)  # Set pilihan default sesuai status saat ini
        self.combo_status.pack(side="left", padx=(0, 15))

        # Tombol Simpan Perubahan Status
        self.btn_update = ctk.CTkButton(
            self.update_frame,
            text="Update Status",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#965829",
            hover_color="#7A451E",
            width=130,
            command=self.simpan_perubahan_status
        )
        self.btn_update.pack(side="left")

        # ----------------- TOMBOL TUTUP / KEMBALI -----------------
        self.btn_close = ctk.CTkButton(
            self.main_card,
            text="Tutup / Pesanan Baru",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#8E5A2A",
            hover_color="#7A451E",
            height=38,
            command=self.destroy
        )
        self.btn_close.pack(pady=(10, 15))

    def simpan_perubahan_status(self):
        """Memperbarui status pesanan secara lokal di GUI (Tanpa Database & Tanpa Controller)"""
        status_baru = self.combo_status.get()

        # Update nilai status di tabel Treeview GUI secara lokal
        item_vals = list(self.tree_info.item("row_1", "values"))
        item_vals[3] = status_baru
        self.tree_info.item("row_1", values=item_vals)

        # Update data internal
        self.order_data["status_pesanan"] = status_baru

        messagebox.showinfo("Informasi", f"Status pesanan berhasil diubah secara lokal menjadi '{status_baru}'!\n(Tidak terhubung ke database/controller)")


if __name__ == "__main__":
    app = OrderStatusView()
    app.mainloop()