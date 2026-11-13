from unittest.mock import MagicMock
from models.menu_model import MenuModel

def test_get_all_menu_berhasil():
    # 1. Inisialisasi Model Menu Warm Coffee
    model = MenuModel()

    # 2. Memanipulasi (Mock) koneksi database agar terisolasi dan tidak menyentuh DB asli
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor

    # 3. Menyiapkan data dummy sesuai tabel menu Warm Coffee Anda
    mock_cursor.fetchall.return_value = [
        {"id_menu": 1, "nama_menu": "Espresso", "kategori": "Kopi", "harga": 18000.00, "stok": 37, "status_menu": "Tersedia"},
        {"id_menu": 2, "nama_menu": "Americano", "kategori": "Kopi", "harga": 22000.00, "stok": 39, "status_menu": "Tersedia"}
    ]

    # 4. Melakukan eksekusi fungsi get_all_menu
    hasil = model.get_all_menu()

    # 5. Verifikasi hasil pengujian (Assertion)
    assert len(hasil) == 2
    assert hasil[0]["nama_menu"] == "Espresso"
    assert hasil[1]["harga"] == 22000.00

    # Memastikan kueri/cursor execute benar-benar dipanggil
    mock_cursor.execute.assert_called_once()