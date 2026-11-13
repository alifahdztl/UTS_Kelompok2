from views.welcome_view import WelcomeView


class AppController:
    """
    Pengendali awal aplikasi (titik masuk dipanggil dari main.py).
    Mengikat tombol pada WelcomeView dengan aksi membuka halaman login yang sesuai peran.
    """

    def __init__(self):
        self.view = WelcomeView()
        self.view.btn_pelanggan.configure(command=self.buka_login_pelanggan)
        self.view.btn_kasir.configure(command=self.buka_login_kasir)

    def buka_login_pelanggan(self):
        from views.login_view import LoginView  # impor di sini agar tidak circular
        self.view.destroy()
        LoginView().mainloop()

    def buka_login_kasir(self):
        from views.login_kasir_barista_view import LoginKasirBaristaView
        self.view.destroy()
        LoginKasirBaristaView().mainloop()

    def run(self):
        self.view.mainloop()
