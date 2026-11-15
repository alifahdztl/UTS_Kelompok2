from controllers.app_controller import AppController

if __name__ == "__main__":
    # Animasi pembuka Kopiloka. Menutup dirinya sendiri, lalu aplikasi dilanjutkan.
    try:
        from views.splash_view import SplashView
        SplashView().mainloop()
    except Exception as e:  # animasi tidak boleh menghalangi aplikasi
        print(f"Splash dilewati: {e}")

    app = AppController()
    app.run()