import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector

ctk.set_appearance_mode("Dark")


class KasirOrderStatusView(ctk.CTk):
    def __init__(self, order_data=None, pelanggan_data=None):
        super().__init__()

        self.order_data = order_data or {}
        self.pelanggan_data = pelanggan_data or {}

        self.title("Warm Coffee - Order Status Kasir / Barista")
        self.geometry("860x540")
        self.resizable(False, False)
        self.configure(fg_color="#1e1411")

        self.main_card = ctk.CTkFrame(self, fg_color="#2b1f1a", corner_radius=15)
        self.main_card.pack(pady=20, padx=20, fill="both", expand=True)

        self.lbl_title = ctk.CTkLabel(
            self.main_card,
            text="PANEL KASIR & BARISTA - KELOLA PESANAN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F5E6D3"
        )
        self.lbl_title.pack(pady=(20, 15))

        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Kasir.Treeview",
            background="#1e1411",
            foreground="#F5E6D3",
            rowheight=35,
            fieldbackground="#1e1411"
        )
        style.configure(
            "Kasir.Treeview.Heading",
            background="#8E5A2A",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold")
        )

        columns = ("no_antrian", "nama_pelanggan", "menu_dipesan", "status_pesanan", "total_harga")
        self.tree_info = ttk.Treeview(
            self.main_card,
            columns=columns,
            show="headings",
            height=4,
            style="Kasir.Treeview"
        )

        self.tree_info.heading("no_antrian", text="No. Antrian")
        self.tree_info.heading("nama_pelanggan", text="Nama Pelanggan")
        self.tree_info.heading("menu_dipesan", text="Menu Dipesan")
        self.tree_info.heading("status_pesanan", text="Status Pesanan")
        self.tree_info.heading("total_harga", text="Total Harga")

        self.tree_info.column("no_antrian", width=90, anchor="center")
        self.tree_info.column("nama_pelanggan", width=140, anchor="w")
        self.tree_info.column("menu_dipesan", width=240, anchor="w")
        self.tree_info.column("status_pesanan", width=130, anchor="center")
        self.tree_info.column("total_harga", width=130, anchor="center")

        self.tree_info.pack(fill="both", expand=True, padx=20, pady=10)

        # Auto-load data saat panel dibuka
        self.load_data_from_db()

        # Kontrol Pengubahan Status Pesanan
        self.control_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        self.control_frame.pack(fill="x", padx=20, pady=10)

        self.lbl_status = ctk.CTkLabel(
            self.control_frame, text="Ubah Status Pesanan:", font=ctk.CTkFont(size=12, weight="bold"), text_color="#F5E6D3"
        )
        self.lbl_status.pack(side="left", padx=(0, 8))

        self.combo_status = ctk.CTkComboBox(
            self.control_frame,
            values=["Pending", "Diproses", "Selesai"],
            width=180,
            fg_color="#1e1411",
            border_color="#8E5A2A",
            button_color="#8E5A2A"
        )
        self.combo_status.set("Pending")
        self.combo_status.pack(side="left", padx=(0, 15))

        self.btn_update_status = ctk.CTkButton(
            self.control_frame,
            text="Update Status",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#D35400",
            hover_color="#BA4A00",
            width=110,
            command=self.update_status_pesanan
        )
        self.btn_update_status.pack(side="left")

        # Tombol Refresh Data Pesanan
        self.btn_refresh = ctk.CTkButton(
            self.main_card,
            text="MUAT ULANG DATA PESANAN",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2980B9",
            hover_color="#1F618D",
            height=35,
            command=self.load_data_from_db
        )
        self.btn_refresh.pack(fill="x", padx=20, pady=(10, 5))

        self.btn_close = ctk.CTkButton(
            self.main_card,
            text="Tutup Panel Kasir",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#8E5A2A",
            hover_color="#7A451E",
            height=35,
            command=self.destroy
        )
        self.btn_close.pack(pady=(5, 15), padx=20, fill="x")

    def get_connection(self):
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="database_sistem_informasi_pemesanan_coffe_shop"
            )
        except Exception as e:
            print("Error koneksi database kasir:", e)
            return None

    def load_data_from_db(self):
        """Mengambil data pesanan terbaru dari database MySQL"""
        for row in self.tree_info.get_children():
            self.tree_info.delete(row)

        try:
            conn = self.get_connection()
            if not conn:
                return
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT p.*, pl.nama_pelanggan 
                FROM pemesanan p 
                LEFT JOIN pelanggan pl ON p.id_pelanggan = pl.id_pelanggan 
                ORDER BY p.id_pesanan DESC LIMIT 1
            """)
            order = cursor.fetchone()

            if order:
                self.order_data = order
                
                cursor.execute("""
                    SELECT m.nama_menu, dp.jumlah AS qty 
                    FROM detail_pesanan dp 
                    JOIN menu m ON dp.id_menu = m.id_menu 
                    WHERE dp.id_pesanan = %s
                """, (order.get("id_pesanan"),))
                items = cursor.fetchall()

                menu_text_list = [f"{item.get('nama_menu', 'Menu')} ({item.get('qty', 1)}x)" for item in items]
                daftar_menu_str = ", ".join(menu_text_list) if menu_text_list else "-"

                nomor_antrian = order.get("nomor_antrian", "A-01")
                nama_pelanggan = (order.get("nama_pelanggan") or "Pelanggan").title()
                current_status = order.get("status_pesanan", "Pending")
                total_harga = f"Rp {order.get('total_harga', 0):,}".replace(",", ".")

                self.tree_info.insert("", "end", iid="row_1", values=(
                    nomor_antrian,
                    nama_pelanggan,
                    daftar_menu_str,
                    current_status,
                    total_harga
                ))

            cursor.close()
            conn.close()
        except Exception as e:
            print("Error load database kasir:", e)

    def update_status_pesanan(self):
        if not self.order_data or "id_pesanan" not in self.order_data:
            messagebox.showwarning("Peringatan", "Belum ada data pesanan yang masuk!")
            return

        status_baru = self.combo_status.get()
        pesanan_id = self.order_data.get("id_pesanan")

        try:
            conn = self.get_connection()
            if not conn:
                messagebox.showerror("Error", "Gagal koneksi database!")
                return

            cursor = conn.cursor()
            cursor.execute("""
                UPDATE pemesanan 
                SET status_pesanan = %s 
                WHERE id_pesanan = %s
            """, (status_baru, pesanan_id))
            conn.commit()
            cursor.close()
            conn.close()

            self.load_data_from_db()
            messagebox.showinfo("Sukses", f"Status pesanan berhasil diubah menjadi: {status_baru}")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal update database: {e}")


if __name__ == "__main__":
    app = KasirOrderStatusView()
    app.mainloop()