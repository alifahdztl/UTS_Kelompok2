# ☕ KopiLoka - Sistem Informasi Pemesanan Coffee Shop (MVC Python)
Aplikasi desktop manajemen pemesanan dan layanan pelanggan coffee shop yang dibangun menggunakan arsitektur Model-View-Controller (MVC) dengan bahasa pemrograman Python, antarmuka modern CustomTkinter, serta basis data MySQL.

# 📌 Deskripsi Singkat Aplikasi
KopiLoka dirancang untuk memudahkan pengelolaan operasional kedai kopi secara digital, meliputi sistem autentikasi pelanggan (Sign In & Registrasi), pengelolaan menu produk, transaksi peminjaman/pemesanan, serta pemantauan status pesanan secara real-time berbasis desktop.

# 🗂️ Struktur Direktori MVC
UTS_Kelompok2/
│
├── .github/workflows/  # CI/CD Pipeline (GitHub Actions untuk otomatisasi test)
├── assets/             # Aset visual aplikasi (ikon dan logo KopiLoka)
├── config/             # Konfigurasi koneksi database (database.py)
├── controllers/        # Logika alur aplikasi & manajemen kontroler (LoginController, MenuController, dll)
├── models/             # Interaksi database dan pemrosesan entitas data (Pelanggan, Menu, Pemesanan)
├── tests/              # Unit testing otomatis menggunakan Pytest
├── views/              # Antarmuka pengguna / GUI berbasis CustomTkinter (login_view, menu_view, dll)
├── .gitignore          # Daftar file/folder yang diabaikan oleh Git
├── AplikasiKopiLoka.exe # Berkas eksekusi aplikasi desktop mandiri (hasil build PyInstaller)
├── main.py             # Titik masuk utama (entry point) aplikasi
├── main.spec           # Konfigurasi spesifikasi PyInstaller
├── pytest.ini          # Konfigurasi lingkungan unit testing Pytest
├── requirements.txt    # Daftar pustaka dependensi Python (termasuk customtkinter, mysql-connector, dll)
└── test_model.py       # Berkas pengujian unit model database

