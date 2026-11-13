from config.database import Database


class PemesananModel:
    def __init__(self):
        self.db = Database()
        self.conn = self.db.get_connection()
        self.table_name = "pemesanan"
        self.last_error = None

    def get_all_pemesanan(self):
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"SELECT * FROM {self.table_name}"
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def create_pemesanan(self, id_pelanggan, nomor_antrian, total_harga, status_pesanan):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"INSERT INTO {self.table_name} (id_pelanggan, nomor_antrian, total_harga, status_pesanan) VALUES (%s, %s, %s, %s)"
            val = (id_pelanggan, nomor_antrian, total_harga, status_pesanan)
            cursor.execute(query, val)
            self.conn.commit()
            id_pesanan = cursor.lastrowid
            cursor.close()
            return id_pesanan
        return None

    def get_all_with_pelanggan(self):
        """Semua pesanan beserta nama pelanggan (dipakai panel kasir/barista)."""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"""
                SELECT p.id_pesanan, p.nomor_antrian,
                       IFNULL(pel.nama_pelanggan, 'Umum / Tamu') AS nama_pelanggan,
                       p.tanggal_pesanan, p.status_pesanan, p.total_harga
                FROM {self.table_name} p
                LEFT JOIN pelanggan pel ON p.id_pelanggan = pel.id_pelanggan
            """
            cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        return []

    def get_pesanan_terakhir(self):
        """Pesanan paling baru beserta nama pelanggan, atau None jika belum ada."""
        if self.conn:
            cursor = self.conn.cursor(dictionary=True)
            query = f"""
                SELECT p.*, pl.nama_pelanggan
                FROM {self.table_name} p
                LEFT JOIN pelanggan pl ON p.id_pelanggan = pl.id_pelanggan
                ORDER BY p.id_pesanan DESC LIMIT 1
            """
            cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        return None

    def update_status(self, id_pesanan, status_baru):
        if self.conn:
            cursor = self.conn.cursor()
            query = f"UPDATE {self.table_name} SET status_pesanan = %s WHERE id_pesanan = %s"
            cursor.execute(query, (status_baru, id_pesanan))
            self.conn.commit()
            cursor.close()
            return True
        return False

    def count_pesanan_hari_ini(self):
        """Jumlah pesanan hari ini (dasar pembuatan nomor antrian)."""
        if self.conn:
            cursor = self.conn.cursor()
            query = f"SELECT COUNT(*) FROM {self.table_name} WHERE DATE(tanggal_pesanan) = CURDATE()"
            cursor.execute(query)
            jumlah = cursor.fetchone()[0]
            cursor.close()
            return jumlah
        return 0

    def simpan_pesanan_lengkap(self, id_pelanggan, nomor_antrian, total_harga, status_pesanan, items, kurangi_stok=True):
        """
        Menyimpan pemesanan + detail_pesanan (dan memotong stok menu bila kurangi_stok=True)
        dalam SATU transaksi. Jika salah satu langkah gagal, seluruhnya dibatalkan (rollback).
        Mengembalikan id_pesanan baru, atau None jika gagal.
        """
        if not self.conn:
            return None

        self.last_error = None
        cursor = self.conn.cursor()
        try:
            self.conn.start_transaction()

            cursor.execute(
                f"INSERT INTO {self.table_name} (id_pelanggan, nomor_antrian, total_harga, status_pesanan) VALUES (%s, %s, %s, %s)",
                (id_pelanggan, nomor_antrian, total_harga, status_pesanan)
            )
            id_pesanan = cursor.lastrowid

            for item in items:
                cursor.execute(
                    "INSERT INTO detail_pesanan (id_pesanan, id_menu, jumlah, subtotal) VALUES (%s, %s, %s, %s)",
                    (id_pesanan, item["id_menu"], item["qty"], item["subtotal"])
                )
                if kurangi_stok:
                    cursor.execute(
                        "UPDATE menu SET stok = stok - %s WHERE id_menu = %s AND stok >= %s",
                        (item["qty"], item["id_menu"], item["qty"])
                    )
                    if cursor.rowcount == 0:
                        raise ValueError(f"Stok '{item.get('nama_menu', item['id_menu'])}' tidak mencukupi atau sudah berubah.")

            self.conn.commit()
            return id_pesanan
        except Exception as e:
            self.conn.rollback()
            print(f"Gagal menyimpan pesanan: {e}")
            self.last_error = str(e)
            return None
        finally:
            cursor.close()
