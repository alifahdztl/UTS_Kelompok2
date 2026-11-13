from tkinter import messagebox
from models.pemesanan_model import PemesananModel


class PembayaranController:
    def __init__(self):
        self.pemesanan_model = PemesananModel()

    def proses_pembayaran(self, id_pesanan):
        """Memperbarui status pesanan menjadi Lunas (lewat Model) berdasarkan id_pesanan."""
        if not self.pemesanan_model.conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return False

        try:
            return self.pemesanan_model.update_status(id_pesanan, "Lunas")
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui status pembayaran: {e}")
            return False
