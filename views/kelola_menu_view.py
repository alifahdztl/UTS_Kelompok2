import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from tkinter import ttk, messagebox
from controllers.menu_controller import MenuController

BATAS_STOK_MENIPIS = 5
STATUS_BAWAAN = ["Tersedia", "Habis"]


class KelolaMenuView(ctk.CTkToplevel):
    """
    Jendela untuk Kasir / Barista: melihat daftar menu, mengubah stok/harga/status,
    serta menambah menu baru. Dibuka dari tombol 'Kelola Menu & Stok' di KasirBaristaOrderView.
    """

    def __init__(self, master=None):
        super().__init__(master)

        self.controller = MenuController()
        self.selected_id = None
        self.data_menu = []

        self.title("Warm Coffee - Kelola Menu & Stok (Kasir / Barista)")
        self.geometry("900x650")
        self.resizable(False, False)
        self.configure(fg_color="#231915")

        # Container Utama
        self.main_card = ctk.CTkFrame(self, fg_color="#362822", corner_radius=15)
        self.main_card.pack(pady=20, padx=20, fill="both", expand=True)

        self.lbl_title = ctk.CTkLabel(
            self.main_card,
            text="KELOLA MENU & STOK",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#F5E6D3"
        )
        self.lbl_title.pack(pady=(20, 5))

        self.lbl_info = ctk.CTkLabel(
            self.main_card,
            text=f"Pilih menu di tabel untuk mengubahnya. Stok \u2264 {BATAS_STOK_MENIPIS} ditandai oranye, stok 0 ditandai merah.",
            font=ctk.CTkFont(size=11),
            text_color="#BFA58C"
        )
        self.lbl_info.pack(pady=(0, 10))

        # ----------------- TABEL MENU -----------------
        style = ttk.Style()
        style.configure(
            "Menu.Treeview",
            background="#231915",
            foreground="#F5E6D3",
            rowheight=30,
            fieldbackground="#231915"
        )
        style.configure(
            "Menu.Treeview.Heading",
            background="#8E5A2A",
            foreground="#FFFFFF",
            font=("Arial", 10, "bold")
        )
        style.map(
            "Menu.Treeview",
            background=[("selected", "#8E5A2A")],
            foreground=[("selected", "#FFFFFF")]
        )

        tree_frame = ctk.CTkFrame(self.main_card, fg_color="transparent")
        tree_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        columns = ("id_menu", "nama_menu", "kategori", "harga", "stok", "status_menu")
        self.tree = ttk.Treeview(
            tree_frame,
            columns=columns,
            show="headings",
            height=7,
            style="Menu.Treeview"
        )
        self.tree.heading("id_menu", text="ID")
        self.tree.heading("nama_menu", text="Nama Menu")
        self.tree.heading("kategori", text="Kategori")
        self.tree.heading("harga", text="Harga")
        self.tree.heading("stok", text="Stok")
        self.tree.heading("status_menu", text="Status")

        self.tree.column("id_menu", width=50, anchor="center")
        self.tree.column("nama_menu", width=250, anchor="w")
        self.tree.column("kategori", width=130, anchor="center")
        self.tree.column("harga", width=110, anchor="center")
        self.tree.column("stok", width=70, anchor="center")
        self.tree.column("status_menu", width=110, anchor="center")

        self.tree.tag_configure("menipis", foreground="#F39C12")
        self.tree.tag_configure("habis", foreground="#E74C3C")

        scrollbar = ctk.CTkScrollbar(tree_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.tree.bind("<<TreeviewSelect>>", self.on_pilih_menu)

        # ----------------- FORM EDIT / TAMBAH -----------------
        form = ctk.CTkFrame(self.main_card, fg_color="transparent")
        form.pack(fill="x", padx=20, pady=(0, 5))
        for kolom in range(3):
            form.grid_columnconfigure(kolom, weight=1, uniform="field")

        opsi_entry = dict(
            fg_color="#231915",
            border_color="#8E5A2A",
            text_color="#F5E6D3",
            height=32
        )

        # Baris 1: Nama Menu | Kategori | Harga
        self._label(form, "Nama Menu", 0, 0)
        self.ent_nama = ctk.CTkEntry(form, **opsi_entry)
        self.ent_nama.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(0, 8))

        self._label(form, "Kategori (bisa diketik baru)", 0, 1)
        self.cmb_kategori = ctk.CTkComboBox(
            form,
            values=[],
            fg_color="#231915",
            border_color="#8E5A2A",
            button_color="#8E5A2A",
            button_hover_color="#7A451E",
            dropdown_fg_color="#362822",
            dropdown_hover_color="#8E5A2A",
            dropdown_text_color="#F5E6D3",
            text_color="#F5E6D3",
            height=32
        )
        self.cmb_kategori.set("")
        self.cmb_kategori.grid(row=1, column=1, sticky="ew", padx=(0, 10), pady=(0, 8))

        self._label(form, "Harga (Rp)", 0, 2)
        self.ent_harga = ctk.CTkEntry(form, placeholder_text="contoh: 18000", **opsi_entry)
        self.ent_harga.grid(row=1, column=2, sticky="ew", pady=(0, 8))

        # Baris 2: Stok | Status
        self._label(form, "Stok", 2, 0)
        self.ent_stok = ctk.CTkEntry(form, placeholder_text="contoh: 50", **opsi_entry)
        self.ent_stok.grid(row=3, column=0, sticky="ew", padx=(0, 10))

        self._label(form, "Status Menu", 2, 1)
        self.cmb_status = ctk.CTkOptionMenu(
            form,
            values=list(STATUS_BAWAAN),
            fg_color="#231915",
            button_color="#8E5A2A",
            button_hover_color="#7A451E",
            dropdown_fg_color="#362822",
            dropdown_hover_color="#8E5A2A",
            dropdown_text_color="#F5E6D3",
            text_color="#F5E6D3",
            height=32
        )
        self.cmb_status.set(STATUS_BAWAAN[0])
        self.cmb_status.grid(row=3, column=1, sticky="ew", padx=(0, 10))

        # ----------------- TOMBOL AKSI -----------------
        aksi = ctk.CTkFrame(self.main_card, fg_color="transparent")
        aksi.pack(fill="x", padx=20, pady=(15, 5))
        for kolom in range(4):
            aksi.grid_columnconfigure(kolom, weight=1, uniform="aksi")

        self.btn_simpan = ctk.CTkButton(
            aksi, text="Simpan Perubahan",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#965829", hover_color="#7A451E", height=38,
            command=self.simpan_perubahan
        )
        self.btn_simpan.grid(row=0, column=0, sticky="ew", padx=(0, 6))

        self.btn_tambah = ctk.CTkButton(
            aksi, text="Tambah Menu Baru",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#27AE60", hover_color="#1E8449", height=38,
            command=self.tambah_menu
        )
        self.btn_tambah.grid(row=0, column=1, sticky="ew", padx=6)

        self.btn_kosongkan = ctk.CTkButton(
            aksi, text="Kosongkan Form",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#5D4A3E", hover_color="#4A392F", height=38,
            command=self.kosongkan_form
        )
        self.btn_kosongkan.grid(row=0, column=2, sticky="ew", padx=6)

        self.btn_refresh = ctk.CTkButton(
            aksi, text="Refresh",
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#8E5A2A", hover_color="#7A451E", height=38,
            command=lambda: self.muat_data_menu(pilih_id=self.selected_id)
        )
        self.btn_refresh.grid(row=0, column=3, sticky="ew", padx=(6, 0))

        self.btn_tutup = ctk.CTkButton(
            self.main_card, text="Tutup",
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#C0392B", hover_color="#962D22", height=38,
            command=self.destroy
        )
        self.btn_tutup.pack(fill="x", padx=20, pady=(5, 15))

        self.muat_data_menu()
        self.after(200, self._fokus)

    # ----------------- HELPER TAMPILAN -----------------
    def _label(self, parent, teks, row, column):
        lbl = ctk.CTkLabel(
            parent, text=teks,
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="#F5E6D3", anchor="w"
        )
        lbl.grid(row=row, column=column, sticky="w", pady=(0, 2))
        return lbl

    def _fokus(self):
        """Memastikan jendela muncul di depan jendela kasir."""
        try:
            self.lift()
            self.focus_force()
        except Exception:
            pass

    def _isi_entry(self, entry, nilai):
        entry.delete(0, "end")
        entry.insert(0, str(nilai))

    # ----------------- DATA -----------------
    def muat_data_menu(self, pilih_id=None):
        """Memuat ulang daftar menu dari database melalui MenuController."""
        self.data_menu = self.controller.ambil_semua_menu()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for m in self.data_menu:
            stok = int(m.get("stok") or 0)
            if stok <= 0:
                tag = ("habis",)
            elif stok <= BATAS_STOK_MENIPIS:
                tag = ("menipis",)
            else:
                tag = ()

            self.tree.insert(
                "", "end",
                iid=str(m["id_menu"]),
                values=(
                    m["id_menu"],
                    m["nama_menu"],
                    m.get("kategori"),
                    f"Rp {int(m['harga']):,}".replace(",", "."),
                    stok,
                    m.get("status_menu")
                ),
                tags=tag
            )

        self._perbarui_pilihan()

        if pilih_id is not None and self.tree.exists(str(pilih_id)):
            self.tree.selection_set(str(pilih_id))
            self.tree.see(str(pilih_id))
        else:
            self.selected_id = None

    def _perbarui_pilihan(self):
        """Mengisi pilihan Kategori dan Status dari data yang ada di database."""
        kategori = sorted({m["kategori"] for m in self.data_menu if m.get("kategori")})
        self.cmb_kategori.configure(values=kategori)

        status = list(STATUS_BAWAAN)
        for m in self.data_menu:
            if m.get("status_menu") and m["status_menu"] not in status:
                status.append(m["status_menu"])
        self.cmb_status.configure(values=status)

    # ----------------- EVENT -----------------
    def on_pilih_menu(self, event=None):
        """Mengisi form dengan data menu yang dipilih di tabel."""
        dipilih = self.tree.selection()
        if not dipilih:
            return

        id_menu = int(dipilih[0])
        menu = next((m for m in self.data_menu if m["id_menu"] == id_menu), None)
        if not menu:
            return

        self.selected_id = id_menu
        self._isi_entry(self.ent_nama, menu["nama_menu"])
        self.cmb_kategori.set(menu.get("kategori") or "")
        self._isi_entry(self.ent_harga, int(menu["harga"]))
        self._isi_entry(self.ent_stok, int(menu.get("stok") or 0))
        self.cmb_status.set(menu.get("status_menu") or STATUS_BAWAAN[0])

    def kosongkan_form(self):
        """Mengosongkan form, siap untuk menambah menu baru."""
        self.selected_id = None
        terpilih = self.tree.selection()
        if terpilih:
            self.tree.selection_remove(*terpilih)
        self.ent_nama.delete(0, "end")
        self.cmb_kategori.set("")
        self.ent_harga.delete(0, "end")
        self.ent_stok.delete(0, "end")
        self.cmb_status.set(STATUS_BAWAAN[0])
        self.ent_nama.focus()

    def _ambil_isian_form(self):
        return (
            self.ent_nama.get(),
            self.cmb_kategori.get(),
            self.ent_harga.get(),
            self.ent_stok.get(),
            self.cmb_status.get()
        )

    def simpan_perubahan(self):
        """Menyimpan perubahan pada menu yang sedang dipilih."""
        if self.selected_id is None:
            messagebox.showwarning("Peringatan", "Pilih menu dari tabel terlebih dahulu!")
            return

        nama, kategori, harga, stok, status = self._ambil_isian_form()
        if self.controller.ubah_menu(self.selected_id, nama, kategori, harga, stok, status):
            self.muat_data_menu(pilih_id=self.selected_id)

    def tambah_menu(self):
        """Menambahkan menu baru dari isian form."""
        nama, kategori, harga, stok, status = self._ambil_isian_form()
        if self.controller.tambah_menu_baru(nama, kategori, harga, stok, status):
            self.kosongkan_form()
            self.muat_data_menu()