import hashlib
from unittest.mock import MagicMock
from config.security import hash_password
from models.login_model import LoginModel
from models.signin_model import SigninModel
from models.kasir_barista_model import KasirBaristaModel


def test_hash_password_konsisten():
    password_asli = "rahasia123"
    hash_1 = hash_password(password_asli)
    hash_2 = hash_password(password_asli)

    assert hash_1 != password_asli
    assert hash_1 == hash_2
    assert len(hash_1) == 64  # panjang standar SHA-256
    assert hash_1 == hashlib.sha256(b"rahasia123").hexdigest()


def test_hash_password_berbeda_untuk_input_berbeda():
    assert hash_password("abc123") != hash_password("abc124")


def siapkan_login_model():
    model = LoginModel()
    model.db = MagicMock()
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    model.db.get_connection.return_value = mock_conn
    return model, mock_cursor


def test_login_pelanggan_berhasil():
    model, mock_cursor = siapkan_login_model()
    mock_cursor.fetchone.return_value = {"id_pelanggan": 1, "nama_pelanggan": "Budi", "email": "budi@mail.com"}

    hasil = model.get_pelanggan_by_credentials("Budi", "budi@mail.com", "rahasia123")

    assert hasil["nama_pelanggan"] == "Budi"
    parameter = mock_cursor.execute.call_args[0][1]
    # yang dikirim ke database adalah HASH, bukan password asli
    assert parameter == ("Budi", "budi@mail.com", hash_password("rahasia123"))
    assert "rahasia123" not in parameter


def test_login_pelanggan_gagal_password_salah():
    model, mock_cursor = siapkan_login_model()
    mock_cursor.fetchone.return_value = None

    assert model.get_pelanggan_by_credentials("Budi", "budi@mail.com", "salah") is None


def test_login_pelanggan_tanpa_koneksi():
    model = LoginModel()
    model.db = MagicMock()
    model.db.get_connection.return_value = None

    assert model.get_pelanggan_by_credentials("Budi", "budi@mail.com", "x") is None


def test_registrasi_pelanggan_password_tersimpan_sebagai_hash():
    model = SigninModel()
    model.db = MagicMock()
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value = mock_cursor
    model.db.get_connection.return_value = mock_conn

    hasil = model.insert_pelanggan("Budi", "08123456789", "budi@mail.com", "rahasia123")

    assert hasil is True
    parameter = mock_cursor.execute.call_args[0][1]
    assert parameter[3] == hash_password("rahasia123")
    assert "rahasia123" not in parameter
    mock_conn.commit.assert_called_once()


def test_registrasi_pelanggan_gagal_rollback():
    model = SigninModel()
    model.db = MagicMock()
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_cursor.execute.side_effect = Exception("duplicate entry")
    mock_conn.cursor.return_value = mock_cursor
    model.db.get_connection.return_value = mock_conn

    assert model.insert_pelanggan("Budi", "0812", "budi@mail.com", "rahasia123") is False
    mock_conn.rollback.assert_called_once()


def siapkan_kasir_model():
    model = KasirBaristaModel()
    model.conn = MagicMock()
    mock_cursor = MagicMock()
    model.conn.cursor.return_value = mock_cursor
    return model, mock_cursor


def test_login_kasir_berhasil():
    model, mock_cursor = siapkan_kasir_model()
    mock_cursor.fetchone.return_value = {"nama_kasir": "Sari", "email": "sari@mail.com"}

    hasil = model.login_kasir("Sari", "sari@mail.com", "kopi12345")

    assert hasil["nama_kasir"] == "Sari"
    assert mock_cursor.execute.call_args[0][1] == ("Sari", "sari@mail.com", hash_password("kopi12345"))


def test_registrasi_kasir_password_tersimpan_sebagai_hash():
    model, mock_cursor = siapkan_kasir_model()

    hasil = model.registrasi_kasir("Sari", "sari@mail.com", "0899", "kopi12345")

    assert hasil is True
    parameter = mock_cursor.execute.call_args[0][1]
    assert parameter[3] == hash_password("kopi12345")
    assert "kopi12345" not in parameter
    model.conn.commit.assert_called_once()


def test_get_all_kasir():
    model, mock_cursor = siapkan_kasir_model()
    mock_cursor.fetchall.return_value = [{"nama_kasir": "Sari", "nomor_telepon": "0899", "email": "sari@mail.com"}]

    hasil = model.get_all_kasir()

    assert len(hasil) == 1
    mock_cursor.execute.assert_called_once()
