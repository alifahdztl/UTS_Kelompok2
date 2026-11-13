from tkinter import messagebox
from models.pemesanan_model import PemesananModel
from models.detail_pesanan_model import DetailPesananModel

STATUS_VALID = ("Pending", "Diproses", "Selesai")


class OrderStatusController:
    def __init__(self):
        self.pemesanan_model = PemesananModel()
        self.detail_model = DetailPesananModel()

    def ambil_semua_pesanan(self):
        """Semua pesanan untuk tabel panel kasir/barista."""
        if not self.pemesanan_model.conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return []
        return self.pemesanan_model.get_all_with_pelanggan()

    def ambil_pesanan_terakhir(self):
        """
        Mengambil pesanan terbaru beserta daftar menunya.
        Mengembalikan tuple (order, items); order bernilai None jika belum ada pesanan.
        """
        if not self.pemesanan_model.conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return None, []

        order = self.pemesanan_model.get_pesanan_terakhir()
        if not order:
            return None, []

        items = self.detail_model.get_by_pesanan(order["id_pesanan"])
        return order, items

    def update_status_pesanan(self, id_pesanan, status_baru):
        """
        Memperbarui status pesanan melalui Model.
        Mengembalikan True jika berhasil, atau False jika gagal.
        """
        if not id_pesanan:
            messagebox.showerror("Error", "ID Pesanan tidak valid!")
            return False

        if status_baru not in STATUS_VALID:
            messagebox.showerror("Error", "Status pesanan tidak valid!")
            return False

        if not self.pemesanan_model.conn:
            messagebox.showerror("Error Koneksi", "Tidak terhubung ke database!")
            return False

        try:
            self.pemesanan_model.update_status(id_pesanan, status_baru)
        except Exception as e:
            messagebox.showerror("Error MySQL", f"Gagal update database: {e}")
            return False

        messagebox.showinfo("Berhasil", f"Status pesanan berhasil diubah menjadi '{status_baru}'!")
        return True

    def kirim_pesanan(self, order_data, pelanggan_data):
        """
        Memastikan pesanan sudah tersimpan di database sebelum lanjut ke pembayaran.
        Pesanan dari halaman menu sudah disimpan saat checkout (punya id_pesanan),
        jadi tidak disimpan ulang agar tidak terjadi pesanan ganda.
        Mengembalikan True jika pesanan siap dibayar.
        """
        if not order_data or not order_data.get("items"):
            messagebox.showwarning("Peringatan", "Data pesanan masih kosong!")
            return False

        if order_data.get("id_pesanan"):
            return True

        if not self.pemesanan_model.conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return False

        id_pesanan = self.pemesanan_model.simpan_pesanan_lengkap(
            pelanggan_data.get("id_pelanggan"),
            order_data.get("nomor_antrian", "A-001"),
            order_data.get("total_harga", 0),
            "Pending",
            order_data["items"],
            kurangi_stok=False,
        )
        if id_pesanan is None:
            alasan = self.pemesanan_model.last_error or "terjadi kesalahan database."
            messagebox.showerror("Error Database", f"Gagal mengirim pesanan: {alasan}")
            return False

        order_data["id_pesanan"] = id_pesanan
        messagebox.showinfo("Sukses", "Pesanan berhasil dikirim ke Kasir & Barista!")
        return True
