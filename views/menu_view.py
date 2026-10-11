import sys
import os

# Menambahkan direktori root proyek agar import modul berhasil
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.menu_controller import MenuController  # Pastikan file controller diimport sesuai jalurnya
from views.orderstatus_view import OrderStatusView

ctk.set_appearance_mode("Dark")


class MenuView(ctk.CTk):
    def __init__(self, pelanggan_data=None):
        super().__init__()

        # Inisialisasi Controller
        self.controller = MenuController()

        # Data pelanggan (mengambil data asli atau fallback default)
        self.pelanggan_data = pelanggan_data or {"id_pelanggan": 1, "nama_pelanggan": "Pelanggan"}

        # Konfigurasi Window Utama
        self.title("Warm Coffee - Order & Menu")
        self.geometry("1000x650")
        self.resizable(False, False)
        self.configure(fg_color="#231915")

        self.keranjang = []  # Menyimpan item pesanan sementara

        # Header Section
        self.header_frame = ctk.CTkFrame(self, fg_color="#362822", corner_radius=15)
        self.header_frame.pack(pady=(15, 10), padx=20, fill="x")

        self.label_title = ctk.CTkLabel(
            self.header_frame,
            text=f"WARM COFFEE - SELAMAT DATANG, {self.pelanggan_data['nama_pelanggan'].upper()}!",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#F5E6D3"
        )
        self.label_title.pack(side="left", padx=20, pady=15)

        self.btn_refresh = ctk.CTkButton(
            self.header_frame,
            text="Refresh Menu",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#965829",
            hover_color="#7A451E",
            text_color="#FFFFFF",
            width=120,
            command=self.muat_data_menu
        )
        self.btn_refresh.pack(side="right", padx=20, pady=15)

        # Content Main Container (Kiri: Daftar Menu | Kanan: Keranjang & Pemesanan)
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(pady=5, padx=20, fill="both", expand=True)

        # ----------------- PANEL KIRI: DAFTAR MENU -----------------
        self.left_panel = ctk.CTkFrame(self.content_frame, fg_color="#362822", corner_radius=15)
        self.left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        self.lbl_menu = ctk.CTkLabel(
            self.left_panel, text="Daftar Menu Kopi", font=ctk.CTkFont(size=16, weight="bold"), text_color="#F5E6D3"
        )
        self.lbl_menu.pack(pady=(10, 5))

        # Style Custom untuk Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="#231915", foreground="#F5E6D3", rowheight=28, fieldbackground="#231915")
        style.configure("Treeview.Heading", background="#8E5A2A", foreground="#FFFFFF", font=("Arial", 10, "bold"))
        style.map("Treeview", background=[("selected", "#965829")])

        # Tabel Menu
        columns = ("id_menu", "nama_menu", "harga", "stok")
        self.tree = ttk.Treeview(self.left_panel, columns=columns, show="headings", height=10)
        self.tree.heading("id_menu", text="ID")
        self.tree.heading("nama_menu", text="Nama Menu")
        self.tree.heading("harga", text="Harga")
        self.tree.heading("stok", text="Stok")

        self.tree.column("id_menu", width=40, anchor="center")
        self.tree.column("nama_menu", width=180, anchor="w")
        self.tree.column("harga", width=100, anchor="e")
        self.tree.column("stok", width=60, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Form Tambah ke Keranjang
        self.action_frame = ctk.CTkFrame(self.left_panel, fg_color="transparent")
        self.action_frame.pack(fill="x", padx=10, pady=10)

        self.entry_jumlah = ctk.CTkEntry(
            self.action_frame, placeholder_text="Jumlah Porsi", width=110, fg_color="#231915", border_color="#8E5A2A", text_color="#F5E6D3"
        )
        self.entry_jumlah.pack(side="left", padx=(0, 10))

        self.btn_add = ctk.CTkButton(
            self.action_frame, text="+ Tambah Pesanan", fg_color="#965829", hover_color="#7A451E", command=self.tambah_ke_keranjang
        )
        self.btn_add.pack(side="left", fill="x", expand=True)

        # ----------------- PANEL KANAN: KERANJANG PESANAN -----------------
        self.right_panel = ctk.CTkFrame(self.content_frame, fg_color="#362822", corner_radius=15, width=380)
        self.right_panel.pack(side="right", fill="both", padx=(10, 0))

        self.lbl_cart = ctk.CTkLabel(
            self.right_panel, text="Keranjang Pesanan", font=ctk.CTkFont(size=16, weight="bold"), text_color="#F5E6D3"
        )
        self.lbl_cart.pack(pady=(10, 5))

        # Tabel Keranjang
        cart_cols = ("nama", "qty", "subtotal")
        self.cart_tree = ttk.Treeview(self.right_panel, columns=cart_cols, show="headings", height=8)
        self.cart_tree.heading("nama", text="Menu")
        self.cart_tree.heading("qty", text="Qty")
        self.cart_tree.heading("subtotal", text="Subtotal")

        self.cart_tree.column("nama", width=140, anchor="w")
        self.cart_tree.column("qty", width=50, anchor="center")
        self.cart_tree.column("subtotal", width=100, anchor="e")

        self.cart_tree.pack(fill="both", expand=True, padx=10, pady=5)

        # Label Total & Checkout
        self.lbl_total = ctk.CTkLabel(
            self.right_panel, text="Total: Rp 0", font=ctk.CTkFont(size=16, weight="bold"), text_color="#F5E6D3"
        )
        self.lbl_total.pack(pady=5)

        self.btn_checkout = ctk.CTkButton(
            self.right_panel, text="CONFIRM & BAYAR PESANAN", font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#8E5A2A", hover_color="#7A451E", height=40, command=self.proses_checkout
        )
        self.btn_checkout.pack(fill="x", padx=10, pady=(5, 15))

        # Load Menu dari Database via Controller
        self.muat_data_menu()

    def muat_data_menu(self):
        """Memuat data menu dari database melalui MenuController"""
        for row in self.tree.get_children():
            self.tree.delete(row)

        daftar_menu = self.controller.ambil_semua_menu()

        for item in daftar_menu:
            self.tree.insert("", "end", values=(
                item['id_menu'], 
                item['nama_menu'], 
                f"Rp {float(item['harga']):,.0f}", 
                item['stok']
            ))

    def tambah_ke_keranjang(self):
        """Memindahkan item yang dipilih ke tabel keranjang"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("Peringatan", "Pilih menu dari tabel sebelah kiri terlebih dahulu!")
            return

        jumlah_str = self.entry_jumlah.get().strip()
        if not jumlah_str.isdigit() or int(jumlah_str) <= 0:
            messagebox.showwarning("Peringatan", "Masukkan jumlah porsi angka yang valid!")
            return

        qty = int(jumlah_str)
        item_data = self.tree.item(selected_item[0])['values']
        id_menu, nama_menu, harga_str, stok = item_data[0], item_data[1], str(item_data[2]), int(item_data[3])

        item_existing = next(
            (it for it in self.keranjang if str(it['id_menu']) == str(id_menu)), None
        )
        qty_di_keranjang = item_existing['qty'] if item_existing else 0

        if qty_di_keranjang + qty > stok:
            messagebox.showerror("Stok Tidak Cukup", "Jumlah melebihi stok yang tersedia!")
            return

        harga_clean = float(harga_str.replace("Rp ", "").replace(".", "").replace(",", ""))

        if item_existing:
            item_existing['qty'] += qty
            item_existing['subtotal'] = item_existing['harga'] * item_existing['qty']
        else:
            self.keranjang.append({
                "id_menu": id_menu,
                "nama_menu": nama_menu,
                "harga": harga_clean,
                "qty": qty,
                "subtotal": harga_clean * qty
            })

        self.update_keranjang_ui()
        self.entry_jumlah.delete(0, 'end')

    def update_keranjang_ui(self):
        """Update Tampilan Tabel Keranjang & Total Bayar"""
        for row in self.cart_tree.get_children():
            self.cart_tree.delete(row)

        total = 0
        for item in self.keranjang:
            total += item['subtotal']
            self.cart_tree.insert("", "end", values=(
                item['nama_menu'], item['qty'], f"Rp {item['subtotal']:,.0f}"
            ))

        self.lbl_total.configure(text=f"Total: Rp {total:,.0f}")

    def proses_checkout(self):
        """Memproses checkout pesanan menggunakan MenuController ke database"""
        if not self.keranjang:
            messagebox.showwarning("Keranjang Kosong", "Pilih menu dan masukkan ke keranjang dulu!")
            return

        id_pelanggan = self.pelanggan_data.get("id_pelanggan", 1)
        
        # Panggil fungsi proses checkout dari controller
        order_data = self.controller.proses_pesanan_checkout(id_pelanggan, self.keranjang)

        if order_data:
            # Tutup window menu
            self.destroy()

            # Buka OrderStatusView dengan data dari database
            app_status = OrderStatusView(order_data=order_data, pelanggan_data=self.pelanggan_data)
            app_status.mainloop()


if __name__ == "__main__":
    app = MenuView()
    app.mainloop()