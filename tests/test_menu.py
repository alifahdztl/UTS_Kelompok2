from unittest.mock import MagicMock
from models.menu_model import MenuModel

def test_get_all_menu_berhasil():
    # 1. Inisialisasi Model Menu Warm Coffee
    model = MenuModel()

    # 2. Memanipulasi (Mock) koneksi database agar terisolasi dan tidak menyentuh DB asli
from models.menu_model import MenuModel  # Sesuaikan dengan path model menu Anda

def test_create_menu_berhasil():
    # Menginisialisasi Model Menu
    model = MenuModel()

    # Memanipulasi (Mock) koneksi database agar tidak mengotori data asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Melakukan eksekusi fungsi create_menu sesuai kolom database (nama_menu, kategori, harga, stok, status_menu)
    hasil = model.create_menu("Kopi Susu Gula Aren", "Minuman", 18000.00, 47, "Tersedia")

    # Memverifikasi apakah fungsi mengembalikan nilai True
    assert hasil is True

    # Memverifikasi apakah cursor.execute benar-benar dipanggil sekali
    mock_cursor.execute.assert_called_once()

    # Memverifikasi apakah perintah commit (simpan) dipanggil
    model.conn.commit.assert_called_once()

def test_get_all_menu():
    # Menginisialisasi Model Menu untuk menguji pengambilan data
    model = MenuModel()

    # Memanipulasi (Mock) koneksi database
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # Menyiapkan data dummy yang merepresentasikan isi tabel database Anda
    mock_cursor.fetchall.return_value = [
        {"id_menu": 1, "nama_menu": "Espresso", "kategori": "Kopi", "harga": 18000.00, "stok": 37, "status_menu": "Tersedia"},
        {"id_menu": 9, "nama_menu": "Kopi Susu Gula Aren", "kategori": "Minuman", "harga": 18000.00, "stok": 67, "status_menu": "Tersedia"}
    ]

    # Melakukan eksekusi fungsi get_all_menu
    hasil = model.get_all_menu()

    # Memverifikasi apakah jumlah dan isi data sesuai dengan database
    assert len(hasil) == 2
    assert hasil[0]["nama_menu"] == "Espresso"
    assert hasil[1]["nama_menu"] == "Kopi Susu Gula Aren"
    assert hasil[1]["kategori"] == "Minuman"
    
    # Memverifikasi apakah cursor.execute dipanggil untuk mengambil data
    mock_cursor.execute.assert_called_once()