from tkinter import messagebox
from config.database import Database

class MenuController:
    def __init__(self):
        self.db = Database()

    def ambil_semua_menu(self):
        """
        Mengambil seluruh daftar menu yang tersedia dari database secara berurutan.
        Mengembalikan list dictionary berisi data menu, atau list kosong jika gagal.
        """
        conn = self.db.get_connection()
        if not conn:
            messagebox.showerror("Error", "Gagal terhubung ke database!")
            return []

        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM menu ORDER BY id_menu ASC")
            daftar_menu = cursor.fetchall()
            
            cursor.close()
            conn.close()
            return daftar_menu

        except Exception as e:
            messagebox.showerror("Error", f"Terjadi kesalahan saat memuat menu: {e}")
            return []

    def buat_nomor_antrian(self, cursor):
        """
        Menghasilkan nomor antrian otomatis dengan format A-001 berdasarkan urutan transaksi harian.
        """
        cursor.execute("SELECT COUNT(*) FROM pemesanan WHERE DATE(tanggal_pesanan) = CURDATE()")
        jumlah_hari_ini = cursor.fetchone()[0]
        nomor_baru = jumlah_hari_ini + 1
        return f"A-{nomor_baru:03d}"

    def proses_pesanan_checkout(self, id_pelanggan, keranjang):
        """
        Memproses penyimpanan pesanan ke tabel pemesanan dan detail_pesanan,
        serta melakukan pengurangan stok menu di database secara aman.
        Mengembalikan dictionary data transaksi jika sukses, atau None jika gagal.
        """
        if not keranjang:
            messagebox.showwarning("Keranjang Kosong", "Pilih menu dan masukkan ke keranjang dulu!")
            return None

        conn = self.db.get_connection()
        if not conn:
            messagebox.showerror("Error Koneksi", "Tidak dapat terhubung ke database.")
            return None

        cursor = None
        try:
            cursor = conn.cursor()
            total_harga = sum(item['subtotal'] for item in keranjang)

            nomor_antrian = self.buat_nomor_antrian(cursor)
            status_pesanan = "Pending"

            # 1. Insert transaksi pemesanan
            cursor.execute(
                "INSERT INTO pemesanan (id_pelanggan, nomor_antrian, total_harga, status_pesanan) VALUES (%s, %s, %s, %s)",
                (id_pelanggan, nomor_antrian, total_harga, status_pesanan)
            )

            id_pesanan = cursor.lastrowid

            # 2. Insert detail pesanan & potong stok
            for item in keranjang:
                cursor.execute(
                    "INSERT INTO detail_pesanan (id_pesanan, id_menu, jumlah, subtotal) VALUES (%s, %s, %s, %s)",
                    (id_pesanan, item['id_menu'], item['qty'], item['subtotal'])
                )

                cursor.execute(
                    "UPDATE menu SET stok = stok - %s WHERE id_menu = %s AND stok >= %s",
                    (item['qty'], item['id_menu'], item['qty'])
                )
                if cursor.rowcount == 0:
                    raise Exception(f"Stok '{item['nama_menu']}' tidak mencukupi atau sudah berubah.")

            conn.commit()
            messagebox.showinfo("Sukses", "Pesanan berhasil dibuat!")

            # Kemas data ringkasan transaksi
            order_data = {
                "id_pesanan": id_pesanan,
                "nomor_antrian": nomor_antrian,
                "status_pesanan": status_pesanan,
                "total_harga": total_harga,
                "items": list(keranjang)
            }
            return order_data

        except Exception as e:
            conn.rollback()
            messagebox.showerror("Error Checkout", f"Gagal memproses pesanan: {e}")
            return None
        finally:
            if cursor:
                cursor.close()
            conn.close()