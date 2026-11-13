from unittest.mock import MagicMock
from models.pemesanan_model import PemesananModel
from models.detail_pesanan_model import DetailPesananModel

KERANJANG = [
    {"id_menu": 1, "nama_menu": "Espresso", "qty": 2, "subtotal": 36000.0},
    {"id_menu": 3, "nama_menu": "Caffe Latte", "qty": 1, "subtotal": 28000.0},
]


def siapkan_model():
    model = PemesananModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    return model, mock_cursor


def test_simpan_pesanan_lengkap_berhasil():
    model, mock_cursor = siapkan_model()
    mock_cursor.lastrowid = 77
    mock_cursor.rowcount = 1  # stok berhasil dipotong

    hasil = model.simpan_pesanan_lengkap(1, "A-001", 64000.0, "Pending", KERANJANG)

    assert hasil == 77
    model.conn.start_transaction.assert_called_once()
    # 1 insert pemesanan + (insert detail + update stok) x 2 item = 5 eksekusi
    assert mock_cursor.execute.call_count == 5
    model.conn.commit.assert_called_once()
    model.conn.rollback.assert_not_called()


def test_simpan_pesanan_lengkap_stok_kurang_rollback():
    model, mock_cursor = siapkan_model()
    mock_cursor.lastrowid = 78
    mock_cursor.rowcount = 0  # UPDATE stok tidak mengubah baris -> stok tidak cukup

    hasil = model.simpan_pesanan_lengkap(1, "A-002", 36000.0, "Pending", KERANJANG[:1])

    assert hasil is None
    model.conn.rollback.assert_called_once()
    model.conn.commit.assert_not_called()
    assert "Espresso" in model.last_error


def test_simpan_pesanan_tanpa_koneksi_mengembalikan_none():
    model = PemesananModel()
    model.conn = None

    assert model.simpan_pesanan_lengkap(1, "A-001", 1000, "Pending", KERANJANG) is None


def test_update_status_berhasil():
    model, mock_cursor = siapkan_model()

    hasil = model.update_status(5, "Diproses")

    assert hasil is True
    args = mock_cursor.execute.call_args[0]
    assert args[1] == ("Diproses", 5)  # parameterized query
    model.conn.commit.assert_called_once()


def test_count_pesanan_hari_ini():
    model, mock_cursor = siapkan_model()
    mock_cursor.fetchone.return_value = (3,)

    assert model.count_pesanan_hari_ini() == 3
    mock_cursor.execute.assert_called_once()


def test_get_pesanan_terakhir():
    model, mock_cursor = siapkan_model()
    mock_cursor.fetchone.return_value = {"id_pesanan": 9, "nomor_antrian": "A-004", "nama_pelanggan": "Budi"}

    hasil = model.get_pesanan_terakhir()

    assert hasil["id_pesanan"] == 9
    assert hasil["nama_pelanggan"] == "Budi"


def test_get_detail_by_pesanan():
    model = DetailPesananModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    mock_cursor.fetchall.return_value = [{"nama_menu": "Espresso", "qty": 2}]

    hasil = model.get_by_pesanan(9)

    assert hasil == [{"nama_menu": "Espresso", "qty": 2}]
    assert mock_cursor.execute.call_args[0][1] == (9,)
