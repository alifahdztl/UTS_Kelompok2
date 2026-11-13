import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from config.database import Database
from controllers.orderstatus_controller import OrderStatusController
from views.pembayaran_view import PembayaranView

ctk.set_appearance_mode("Dark")


class KasirBaristaOrderView(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.db = Database()
        self.conn = self.db.get_connection()
        self.controller = OrderStatusController()
        self.selected_id = None
        self.selected_order_data = {}

        # Konfigurasi Window Kasir / Barista
        self.title("Warm Coffee - Informasi & Status Pesanan (Kasir / Barista)")
        self.geometry("820x540")
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

        # Style Custom untuk Treeview
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

        # Tabel Informasi Pesanan Kasir
        columns = ("id_pesanan", "no_antrian", "nama_pelanggan", "tanggal_pesanan", "status_pesanan")
        self.tree_info = ttk.Treeview(
            self.main_card,
            columns=columns,
            show="headings",
            height=5,
            style="Status.Treeview"
        )

        self.tree_info.heading("id_pesanan", text="ID")
        self.tree_info.heading("no_antrian", text="No. Antrian")
        self.tree_info.heading("nama_pelanggan", text="Nama Pelanggan")
        self.tree_info.heading("tanggal_pesanan", text="Tanggal Pesanan")
        self.tree_info.heading("status_pesanan", text="Status Pesanan")

        self.tree_info.column("id_pesanan", width=50, anchor="center")
        self.tree_info.column("no_antrian", width=110, anchor="center")
        self.tree_info.column("nama_pelanggan", width=200, anchor="w")
        self.tree_info.column("tanggal_pesanan", width=180, anchor="center")
        self.tree_info.column("status_pesanan", width=130, anchor="center")

        self.tree_info.pack(fill="both", expand=True, padx=20, pady=10)
        self.tree_info.bind("<ButtonRelease-1>", self.on_select_order)

        # ----------------- PANEL UBAH STATUS PESANAN (KASIR) -----------------
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
        self.combo_status.set("Pending")
        self.combo_status.pack(side="left", padx=(0, 15))

        # Tombol Simpan Perubahan Status ke Database
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

        # ----------------- TOMBOL BAYAR PESANAN -----------------
        self.btn_bayar = ctk.CTkButton(
            self.main_card,
            text="BAYAR PESANAN",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#27AE60",
            hover_color="#1E8449",
            height=38,
            command=self.buka_halaman_pembayaran
        )
        self.btn_bayar.pack(fill="x", padx=20, pady=(5, 5))

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
        self.btn_close.pack(pady=(5, 15), padx=20, fill="x")
        self.btn_close.pack(pady=(5, 5), padx=20, fill="x")

        # ----------------- TOMBOL LOGOUT -----------------
        self.btn_logout = ctk.CTkButton(
            self.main_card,
            text="Logout",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#C0392B",
            hover_color="#962D22",
            height=38,
            command=self.logout
        )
        self.btn_logout.pack(pady=(5, 15), padx=20, fill="x")

        self.load_data_pesanan()

    def load_data_pesanan(self):
        """Mengambil data pesanan dari database (tabel pemesanan)"""
        for item in self.tree_info.get_children():
            self.tree_info.delete(item)
            
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = """
                SELECT p.id_pesanan, p.nomor_antrian, 
                       IFNULL(pel.nama_pelanggan, 'Umum / Tamu') AS nama_pelanggan, 
                       p.tanggal_pesanan, p.status_pesanan, p.total_harga
                FROM pemesanan p
                LEFT JOIN pelanggan pel ON p.id_pelanggan = pel.id_pelanggan
            """
            cursor.execute(query)
            rows = cursor.fetchall()
            cursor.close()
            
            for row in rows:
                self.tree_info.insert("", "end", values=(
                    row.get("id_pesanan"),
                    row.get("nomor_antrian"),
                    row.get("nama_pelanggan"),
                    row.get("tanggal_pesanan"),
                    row.get("status_pesanan")
                ))
        """Mengambil data pesanan melalui OrderStatusController"""
        for item in self.tree_info.get_children():
            self.tree_info.delete(item)

        for row in self.controller.ambil_semua_pesanan():
            self.tree_info.insert("", "end", values=(
                row.get("id_pesanan"),
                row.get("nomor_antrian"),
                row.get("nama_pelanggan"),
                row.get("tanggal_pesanan"),
                row.get("status_pesanan")
            ))

    def on_select_order(self, event):
        selected = self.tree_info.selection()
        if selected:
            values = self.tree_info.item(selected[0], "values")
            self.selected_id = values[0]
            status_val = values[4]
            if status_val in ["Pending", "Diproses", "Selesai"]:
                self.combo_status.set(status_val)
            
            self.selected_order_data = {
                "id_pesanan": values[0],
                "nomor_antrian": values[1],
                "nama_pelanggan": values[2],
                "tanggal_pesanan": values[3],
                "status_pesanan": values[4]
            }

    def simpan_perubahan_status(self):
        """Memperbarui status pesanan langsung di database"""
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih pesanan terlebih dahulu dari tabel!")
            return
            
        status_baru = self.combo_status.get()
        if self.conn:
            cursor = self.conn.cursor()
            query = "UPDATE pemesanan SET status_pesanan = %s WHERE id_pesanan = %s"
            cursor.execute(query, (status_baru, self.selected_id))
            self.conn.commit()
            cursor.close()
            
            messagebox.showinfo("Informasi", f"Status pesanan berhasil diubah menjadi '{status_baru}' di database!")
            self.load_data_pesanan()

        """Memperbarui status pesanan melalui OrderStatusController"""
        if not self.selected_id:
            messagebox.showwarning("Peringatan", "Pilih pesanan terlebih dahulu dari tabel!")
            return

        status_baru = self.combo_status.get()
        if self.controller.update_status_pesanan(self.selected_id, status_baru):
            self.load_data_pesanan()

    def logout(self):
        """Menutup panel kasir dan mengembalikan pengguna ke halaman Login Kasir & Barista"""
        self.destroy()
        from views.login_kasir_barista_view import LoginKasirBaristaView  # impor di sini agar tidak circular
        app_login = LoginKasirBaristaView()
        app_login.mainloop()

    def buka_halaman_pembayaran(self):
        if not self.selected_order_data:
            messagebox.showwarning("Peringatan", "Pilih pesanan yang ingin diproses pembayarannya terlebih dahulu!")
            return
            
        self.destroy()
        app_pembayaran = PembayaranView(
            order_data=self.selected_order_data, 
            pelanggan_data={"nama_pelanggan": self.selected_order_data.get("nama_pelanggan")}
        )
        app_pembayaran.mainloop()


if __name__ == "__main__":
    app = KasirBaristaOrderView()
    app.mainloop()