from tkinter import messagebox
from config.database import Database

class OrderStatusController:
    def __init__(self):
        self.db = Database()

    def update_status_pesanan(self, id_pesanan, status_baru):
        """
        Memperbarui status pesanan di database MySQL berdasarkan id_pesanan.
        Mengembalikan True jika berhasil, atau False jika gagal.
        """
        if not id_pesanan:
            messagebox.showerror("Error", "ID Pesanan tidak valid!")
            return False

        conn = self.db.get_connection()
        if not conn:
            messagebox.showerror("Error Koneksi", "Tidak terhubung ke database!")
            return False

        cursor = None
        try:
            cursor = conn.cursor()
            query = "UPDATE pemesanan SET status_pesanan = %s WHERE id_pesanan = %s"
            cursor.execute(query, (status_baru, id_pesanan))
            conn.commit()

            messagebox.showinfo("Berhasil", f"Status pesanan berhasil diubah menjadi '{status_baru}'!")
            return True

        except Exception as e:
            if conn:
                conn.rollback()
            messagebox.showerror("Error MySQL", f"Gagal update database: {e}")
            return False
            
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()