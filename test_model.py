from models.menu_model import MenuModel
from models.pelanggan_model import PelangganModel
from models.pemesanan_model import PemesananModel
from models.detail_pesanan_model import DetailPesananModel
from models.pembayaran_model import PembayaranModel

print("=== PENGUJIAN MODEL WARM COFFEE (BERDASARKAN DATA AKTUAL) ===\n")

# 1. Menguji MenuModel
print("--- 1. Data Menu ---")
menu_model = MenuModel()
daftar_menu = menu_model.get_all_menu()
for m in daftar_menu:
    print(f"[{m['id_menu']}] {m['nama_menu']} ({m['kategori']}) - Rp {m['harga']} | Stok: {m['stok']} | {m['status_menu']}")

# 2. Menguji PelangganModel
print("\n--- 2. Data Pelanggan ---")
pelanggan_model = PelangganModel()
daftar_pelanggan = pelanggan_model.get_all_pelanggan()
for p in daftar_pelanggan:
    print(f"[{p['id_pelanggan']}] {p['nama_pelanggan']} - {p['nomor_telepon']} - {p['email']}")

# 3. Menguji PemesananModel
print("\n--- 3. Data Pemesanan ---")
pemesanan_model = PemesananModel()
daftar_pemesanan = pemesanan_model.get_all_pemesanan()
for pem in daftar_pemesanan:
    print(f"[{pem['id_pesanan']}] Pelanggan ID: {pem['id_pelanggan']} | No Antrian: {pem['nomor_antrian']} | Tanggal: {pem['tanggal_pesanan']} | Total: Rp {pem['total_harga']} | Status: {pem['status_pesanan']}")

# 4. Menguji DetailPesananModel
print("\n--- 4. Data Detail Pesanan ---")
detail_model = DetailPesananModel()
daftar_detail = detail_model.get_all_detail_pesanan()
for d in daftar_detail:
    print(f"[Detail ID: {d['id_detail']}] Pesanan ID: {d['id_pesanan']} | Menu ID: {d['id_menu']} | Jumlah: {d['jumlah']} | Subtotal: Rp {d['subtotal']}")

# 5. Menguji PembayaranModel
print("\n--- 5. Data Pembayaran ---")
pembayaran_model = PembayaranModel()
daftar_pembayaran = pembayaran_model.get_all_pembayaran()
for bayar in daftar_pembayaran:
    print(f"[Pembayaran ID: {bayar['id_pembayaran']}] Pesanan ID: {bayar['id_pesanan']} | Metode: {bayar['metode_pembayaran']} | Bayar: Rp {bayar['jumlah_bayar']} | Kembali: Rp {bayar['kembalian']} | Status: {bayar['status_pembayaran']}")

print("\n=== PENGUJIAN SELESAI ===")