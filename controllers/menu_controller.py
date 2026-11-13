from tkinter import messagebox
from models.menu_model import MenuModel
from models.pemesanan_model import PemesananModel


class MenuController:
    def __init__(self):
        self.menu_model = MenuModel()
        self.pemesanan_model = PemesananModel()

    def ambil_semua_menu(self):
        """
        Mengambil seluruh daftar menu dari Model.
        Mengembalikan list dictionary berisi data menu, atau list kosong jika gagal.
        """
        if not self.menu_model.conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return []

        try:
            return self.menu_model.get_all_menu()
        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat menu: {e}")
            return []

    def buat_nomor_antrian(self):
        """Nomor antrian otomatis format A-001 berdasarkan jumlah transaksi hari ini."""
        nomor_baru = self.pemesanan_model.count_pesanan_hari_ini() + 1
        return f"A-{nomor_baru:03d}"

    def proses_pesanan_checkout(self, id_pelanggan, keranjang):
        """
        Menyimpan pesanan (pemesanan + detail_pesanan + pengurangan stok) lewat Model.
        Mengembalikan dictionary data transaksi jika sukses, atau None jika gagal.
        """
        if not keranjang:
            messagebox.showwarning("Keranjang Kosong", "Pilih menu dan masukkan ke keranjang dulu!")
            return None

        if not self.pemesanan_model.conn:
            messagebox.showerror("Error Koneksi", "Tidak dapat terhubung ke database.")
            return None

        total_harga = sum(item["subtotal"] for item in keranjang)
        nomor_antrian = self.buat_nomor_antrian()
        status_pesanan = "Pending"

        id_pesanan = self.pemesanan_model.simpan_pesanan_lengkap(
            id_pelanggan, nomor_antrian, total_harga, status_pesanan, keranjang
        )

        if id_pesanan is None:
            alasan = self.pemesanan_model.last_error or "terjadi kesalahan database."
            messagebox.showerror("Error Checkout", f"Gagal memproses pesanan: {alasan}")
            return None

        messagebox.showinfo("Sukses", "Pesanan berhasil dibuat!")
        return {
            "id_pesanan": id_pesanan,
            "nomor_antrian": nomor_antrian,
            "status_pesanan": status_pesanan,
            "total_harga": total_harga,
            "items": list(keranjang),
        }
    # ----------------- KELOLA MENU & STOK (KASIR / BARISTA) -----------------
    def _validasi_data_menu(self, nama_menu, kategori, harga, stok):
        """
        Memvalidasi isian form menu.
        Mengembalikan (nama_menu, kategori, harga, stok) yang sudah bersih, atau None jika tidak valid.
        """
        nama_menu = (nama_menu or "").strip()
        kategori = (kategori or "").strip()
        harga = str(harga).strip()
        stok = str(stok).strip()

        if not nama_menu or not kategori:
            messagebox.showwarning("Peringatan", "Nama menu dan kategori harus diisi!")
            return None

        if not harga.isdigit():
            messagebox.showwarning("Peringatan", "Harga harus berupa angka bulat tanpa titik/koma (contoh: 18000)!")
            return None

        if not stok.isdigit():
            messagebox.showwarning("Peringatan", "Stok harus berupa bilangan bulat 0 atau lebih!")
            return None

        return nama_menu, kategori, int(harga), int(stok)

    def ubah_menu(self, id_menu, nama_menu, kategori, harga, stok, status_menu):
        """Memperbarui data menu (nama, kategori, harga, stok, status). Mengembalikan True jika berhasil."""
        if id_menu is None:
            messagebox.showwarning("Peringatan", "Pilih menu dari tabel terlebih dahulu!")
            return False

        data = self._validasi_data_menu(nama_menu, kategori, harga, stok)
        if data is None:
            return False
        nama_menu, kategori, harga, stok = data

        if not self.menu_model.conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return False

        try:
            self.menu_model.update_menu(id_menu, nama_menu, kategori, harga, stok, status_menu)
            messagebox.showinfo("Sukses", f"Menu '{nama_menu}' berhasil diperbarui!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui menu: {e}")
            return False

    def tambah_menu_baru(self, nama_menu, kategori, harga, stok, status_menu):
        """Menambahkan menu baru ke database. Mengembalikan True jika berhasil."""
        data = self._validasi_data_menu(nama_menu, kategori, harga, stok)
        if data is None:
            return False
        nama_menu, kategori, harga, stok = data

        if not self.menu_model.conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return False

        try:
            self.menu_model.create_menu(nama_menu, kategori, harga, stok, status_menu)
            messagebox.showinfo("Sukses", f"Menu '{nama_menu}' berhasil ditambahkan!")
            return True
        except Exception as e:
            messagebox.showerror("Error", f"Gagal menambahkan menu: {e}")
            return False