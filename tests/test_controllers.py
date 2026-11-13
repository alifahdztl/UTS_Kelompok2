from unittest.mock import MagicMock, patch
from controllers.login_controller import LoginController
from controllers.signin_controller import SigninController
from controllers.menu_controller import MenuController
from controllers.orderstatus_controller import OrderStatusController


def test_login_controller_field_kosong_ditolak():
    with patch("controllers.login_controller.LoginModel") as MockModel, \
            patch("controllers.login_controller.messagebox") as mock_box:
        controller = LoginController()

        hasil = controller.verifikasi_login("Budi", "", "rahasia123")

        assert hasil is None
        mock_box.showwarning.assert_called_once()
        MockModel.return_value.get_pelanggan_by_credentials.assert_not_called()


def test_login_controller_berhasil_mengembalikan_data_pelanggan():
    with patch("controllers.login_controller.LoginModel") as MockModel, \
            patch("controllers.login_controller.messagebox") as mock_box:
        MockModel.return_value.get_pelanggan_by_credentials.return_value = {"nama_pelanggan": "Budi"}
        controller = LoginController()

        hasil = controller.verifikasi_login("Budi", "budi@mail.com", "rahasia123")

        assert hasil == {"nama_pelanggan": "Budi"}
        mock_box.showinfo.assert_called_once()


def test_login_controller_password_salah():
    with patch("controllers.login_controller.LoginModel") as MockModel, \
            patch("controllers.login_controller.messagebox") as mock_box:
        MockModel.return_value.get_pelanggan_by_credentials.return_value = None
        controller = LoginController()

        assert controller.verifikasi_login("Budi", "budi@mail.com", "salah") is None
        mock_box.showerror.assert_called_once()


def test_signin_controller_password_terlalu_pendek():
    with patch("controllers.signin_controller.SigninModel") as MockModel, \
            patch("controllers.signin_controller.messagebox") as mock_box:
        controller = SigninController()

        hasil = controller.registrasi_pelanggan("Budi", "budi@mail.com", "0812", "123")

        assert hasil is False
        mock_box.showwarning.assert_called_once()
        MockModel.return_value.insert_pelanggan.assert_not_called()


def test_signin_controller_berhasil():
    with patch("controllers.signin_controller.SigninModel") as MockModel, \
            patch("controllers.signin_controller.messagebox"):
        MockModel.return_value.insert_pelanggan.return_value = True
        controller = SigninController()

        assert controller.registrasi_pelanggan("Budi", "budi@mail.com", "0812", "rahasia123") is True
        MockModel.return_value.insert_pelanggan.assert_called_once_with("Budi", "0812", "budi@mail.com", "rahasia123")


def test_menu_controller_checkout_berhasil():
    keranjang = [{"id_menu": 1, "nama_menu": "Espresso", "qty": 2, "subtotal": 36000.0}]
    with patch("controllers.menu_controller.MenuModel"), \
            patch("controllers.menu_controller.PemesananModel") as MockPesanan, \
            patch("controllers.menu_controller.messagebox"):
        model = MockPesanan.return_value
        model.count_pesanan_hari_ini.return_value = 4
        model.simpan_pesanan_lengkap.return_value = 12
        controller = MenuController()

        hasil = controller.proses_pesanan_checkout(1, keranjang)

        assert hasil["id_pesanan"] == 12
        assert hasil["nomor_antrian"] == "A-005"
        assert hasil["total_harga"] == 36000.0


def test_menu_controller_checkout_keranjang_kosong():
    with patch("controllers.menu_controller.MenuModel"), \
            patch("controllers.menu_controller.PemesananModel"), \
            patch("controllers.menu_controller.messagebox") as mock_box:
        controller = MenuController()

        assert controller.proses_pesanan_checkout(1, []) is None
        mock_box.showwarning.assert_called_once()


def test_menu_controller_checkout_gagal_menampilkan_error():
    keranjang = [{"id_menu": 1, "nama_menu": "Espresso", "qty": 2, "subtotal": 36000.0}]
    with patch("controllers.menu_controller.MenuModel"), \
            patch("controllers.menu_controller.PemesananModel") as MockPesanan, \
            patch("controllers.menu_controller.messagebox") as mock_box:
        model = MockPesanan.return_value
        model.count_pesanan_hari_ini.return_value = 0
        model.simpan_pesanan_lengkap.return_value = None
        model.last_error = "Stok 'Espresso' tidak mencukupi"
        controller = MenuController()

        assert controller.proses_pesanan_checkout(1, keranjang) is None
        mock_box.showerror.assert_called_once()


def test_orderstatus_controller_update_status():
    with patch("controllers.orderstatus_controller.PemesananModel") as MockPesanan, \
            patch("controllers.orderstatus_controller.DetailPesananModel"), \
            patch("controllers.orderstatus_controller.messagebox"):
        controller = OrderStatusController()

        assert controller.update_status_pesanan(5, "Selesai") is True
        MockPesanan.return_value.update_status.assert_called_once_with(5, "Selesai")


def test_orderstatus_controller_status_tidak_valid():
    with patch("controllers.orderstatus_controller.PemesananModel") as MockPesanan, \
            patch("controllers.orderstatus_controller.DetailPesananModel"), \
            patch("controllers.orderstatus_controller.messagebox") as mock_box:
        controller = OrderStatusController()

        assert controller.update_status_pesanan(5, "Hilang") is False
        mock_box.showerror.assert_called_once()
        MockPesanan.return_value.update_status.assert_not_called()


def test_kirim_pesanan_tidak_menyimpan_ulang_jika_sudah_tersimpan():
    order = {"id_pesanan": 12, "items": [{"id_menu": 1, "qty": 1, "subtotal": 18000.0}]}
    with patch("controllers.orderstatus_controller.PemesananModel") as MockPesanan, \
            patch("controllers.orderstatus_controller.DetailPesananModel"), \
            patch("controllers.orderstatus_controller.messagebox"):
        controller = OrderStatusController()

        assert controller.kirim_pesanan(order, {"id_pelanggan": 1}) is True
        MockPesanan.return_value.simpan_pesanan_lengkap.assert_not_called()
