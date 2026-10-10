print("=== Sistem Pemesanan Coffee Shop ===")

# Menampilkan Daftar Menu Kopi
print("Daftar Menu Kopi:")
print("1. Espresso        - Rp 18.000")
print("2. Americano       - Rp 22.000")
print("3. Caffe Latte     - Rp 28.000")
print("4. Cappuccino      - Rp 28.000")
print("5. Mochaccino      - Rp 30.000")
print("6. Caramel Macchiato - Rp 32.000")
print("7. Kopi Kenangan   - Rp 25.000")
print("-" * 35)

# Input transaksi (menghapus titik jika pengguna mengetik titik)
input_harga = input("Masukkan harga kopi yang dipilih (Rp): ").replace(".", "")
harga_kopi = int(input_harga)

jumlah = int(input("Masukkan jumlah pesanan: "))

# Perhitungan total harga
total_harga = harga_kopi * jumlah
print(f"Total Harga Pesanan: Rp {total_harga:,.0f}".replace(",", "."))

# Input nominal pembayaran (menghapus titik jika pengguna mengetik titik)
input_bayar = input("Masukkan nominal uang pembayaran (Rp): ").replace(".", "")
jumlah_bayar = int(input_bayar)

kembalian = jumlah_bayar - total_harga

print("=" * 35)
print("=== STRIP PEMBAYARAN COFFEE SHOP ===")
print("Status           : Transaksi Berhasil!")
print(f"Total Bayar      : Rp {jumlah_bayar:,.0f}".replace(",", "."))
print(f"Kembalian        : Rp {kembalian:,.0f}".replace(",", "."))
print("====================================")