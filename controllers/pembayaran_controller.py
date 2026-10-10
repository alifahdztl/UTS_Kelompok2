from tkinter import messagebox
from config.database import Database

class PembayaranController:
    def __init__(self):
        self.db = Database()

    def proses_pembayaran(self, id_pesanan):
        """
        Memperbarui status pesanan di database menjadi Lunas berdasarkan id_pesanan.
        """
        conn = self.db.get_connection()
        if not conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return False

        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE pemesanan SET status_pesanan = 'Lunas' WHERE id_pesanan = %s",
                (id_pesanan,)
            )
            conn.commit()
            cursor.close()
            conn.close()
            return True
            
        except Exception as e:
            messagebox.showerror("Error", f"Gagal memperbarui status pembayaran: {e}")
            return False