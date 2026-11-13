-- Jalankan sekali pada database: database_sistem_informasi_pemesanan_coffe_shop
-- (Modul 7: autentikasi dengan password ter-hash SHA-256)

ALTER TABLE pelanggan     ADD COLUMN password VARCHAR(255) NULL;
ALTER TABLE kasir_barista ADD COLUMN password VARCHAR(255) NULL;

-- Akun lama: password awal = nomor telepon masing-masing (sebelumnya nomor telepon dipakai sebagai "password"),
-- disimpan langsung dalam bentuk hash SHA-256.
UPDATE pelanggan     SET password = SHA2(nomor_telepon, 256) WHERE password IS NULL;
UPDATE kasir_barista SET password = SHA2(nomor_telepon, 256) WHERE password IS NULL;

-- Cek hasilnya: kolom password harus berupa 64 karakter acak, bukan teks biasa.
SELECT id_pelanggan, nama_pelanggan, password FROM pelanggan;
SELECT nama_kasir, password FROM kasir_barista;
