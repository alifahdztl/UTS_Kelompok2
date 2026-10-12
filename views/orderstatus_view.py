import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
import mysql.connector
from views.pembayaran_view import PembayaranView

ctk.set_appearance_mode("Dark")


class OrderStatusView(ctk.CTk):
    def __init__(self, order_data=None, pelanggan_data=None):
        super().__init__()

        self.order_data = order_data or {}
        self.pelanggan_data = pelanggan_data or {}

        self.title("Warm Coffee - Informasi & Status Pesanan")
        self.geometry("820x480")
        self.resizable(False, False)
        self.configure(fg_color="#231915")

        self.main_card = ctk.CTkFrame(self, fg_color="#362822", corner_radius=15)
        self.main_card.pack(pady=20, padx=20, fill="both", expand=True)

        self.lbl_title = ctk.CTkLabel(
            self.main_card,
            text="INFORMASI STATUS PESANAN",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F5E6D3"
        )
        self.lbl_title.pack(pady=(20, 15))

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

        menu_items = self.order_data.get("items", [])
        menu_text_list = [f"{item.get('nama_menu', 'Menu')} ({item.get('qty', item.get('jumlah', 1))}x)" for item in menu_items]
        daftar_menu_str = ", ".join(menu_text_list) if menu_text_list else "-"

        self.current_status = self.order_data.get("status_pesanan", "Pending")
        
        nomor_antrian = self.order_data.get("nomor_antrian", "A-01")
        nama_pelanggan = self.pelanggan_data.get("nama_pelanggan", "Pelanggan")
        if nama_pelanggan != "-":
            nama_pelanggan = nama_pelanggan.title()

        self.tree_info.insert("", "end", iid="row_1", values=(
            nomor_antrian,
            nama_pelanggan,
            daftar_menu_str,
            self.current_status
        ))

        # Tombol Kirim & Bayar Pesanan
        self.btn_bayar = ctk.CTkButton(
            self.main_card,
            text="KIRIM & BAYAR PESANAN",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            height=38,
            command=self.kirim_dan_buka_pembayaran
        )
        self.btn_bayar.pack(fill="x", padx=20, pady=(15, 5))

        self.btn_close = ctk.CTkButton(
            self.main_card,
            text="Tutup / Pesanan Baru",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#8E5A2A",
            hover_color="#7A451E",
            height=38,
            command=self.destroy
        )
        self.btn_close.pack(pady=(5, 20), padx=20, fill="x")

    def get_connection(self):
        """Menghubungkan ke database sesuai nama database asli proyek"""
        try:
            return mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="database_sistem_informasi_pemesanan_coffe_shop"
            )
        except Exception as e:
            print("Detail Error Koneksi:", e)
            return None

    def kirim_dan_buka_pembayaran(self):
        """Menyimpan data pesanan ke database MySQL agar langsung masuk ke panel kasir"""
        if not self.order_data or not self.order_data.get("items"):
            messagebox.showwarning("Peringatan", "Data pesanan masih kosong!")
            return

        conn = self.get_connection()
        if not conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return

        try:
            cursor = conn.cursor()

            id_pelanggan = self.pelanggan_data.get("id_pelanggan")
            nomor_antrian = self.order_data.get("nomor_antrian", "A-01")
            total_harga = self.order_data.get("total_harga", 0)
            status_pesanan = "Pending"

            # 1. Simpan ke tabel pemesanan
            cursor.execute("""
                INSERT INTO pemesanan (id_pelanggan, nomor_antrian, total_harga, status_pesanan)
                VALUES (%s, %s, %s, %s)
            """, (id_pelanggan, nomor_antrian, total_harga, status_pesanan))
            
            id_pesanan_baru = cursor.lastrowid
            self.order_data["id_pesanan"] = id_pesanan_baru

            # 2. Simpan detail item ke tabel detail_pesanan (menggunakan kolom 'jumlah')
            for item in self.order_data.get("items", []):
                id_menu = item.get("id_menu")
                jumlah = item.get("qty", item.get("jumlah", 1))
                subtotal = item.get("subtotal", 0)

                cursor.execute("""
                    INSERT INTO detail_pesanan (id_pesanan, id_menu, jumlah, subtotal)
                    VALUES (%s, %s, %s, %s)
                """, (id_pesanan_baru, id_menu, jumlah, subtotal))

            conn.commit()
            cursor.close()
            conn.close()

            messagebox.showinfo("Sukses", "Pesanan berhasil dikirim ke Kasir & Barista!")

            # Lanjut buka halaman pembayaran
            self.destroy()
            app_pembayaran = PembayaranView(order_data=self.order_data, pelanggan_data=self.pelanggan_data)
            app_pembayaran.mainloop()

        except Exception as e:
            messagebox.showerror("Error Database", f"Gagal mengirim pesanan: {e}")


if __name__ == "__main__":
    app = OrderStatusView()
    app.mainloop()