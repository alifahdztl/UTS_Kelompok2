import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import customtkinter as ctk
from PIL import Image
from views.kopiloka_anim import render, state_at, INTRO_MS, BG_HEX, W, H

SKALA = 5              # perbesaran piksel: kanvas 88x90 -> 440x450 (naikkan/turunkan sesuai layar)
LEBAR, TINGGI = W * SKALA, H * SKALA
FRAME_MS = 33          # jeda antar frame (sekitar 30 fps)
LAJU_BAR = 0.04        # maksimal kenaikan loading bar per frame (supaya bergerak halus)
JEDA_AKHIR_MS = 400    # jeda singkat setelah bar penuh sebelum splash menutup


class SplashView(ctk.CTk):
    """
    Layar pembuka animasi Kopiloka: tampil tanpa bingkai di tengah layar, lalu
    menutup dirinya sendiri setelah animasi dan loading selesai (atau saat diklik).

    tugas : daftar fungsi tanpa argumen yang dijalankan satu per satu setelah intro,
            sehingga loading bar mengikuti kemajuan yang nyata. Kosongkan jika tidak perlu.
    """

    def __init__(self, tugas=None):
        super().__init__()
        self.tugas = list(tugas or [])
        self.jumlah_tugas = len(self.tugas)
        self.tugas_selesai = 0
        self.progress = 0.0
        self.waktu_tutup = None
        self.ditutup = False
        self.job = None
        self.foto = None

        self.overrideredirect(True)                # tanpa bingkai & tombol title bar
        self.attributes("-topmost", True)
        self.configure(fg_color=BG_HEX)

        # taruh di tengah layar (memperhitungkan skala DPI Windows)
        skala = self._get_window_scaling() if hasattr(self, "_get_window_scaling") else 1.0
        x = int((self.winfo_screenwidth() - LEBAR * skala) / 2)
        y = int((self.winfo_screenheight() - TINGGI * skala) / 2)
        self.geometry(f"{LEBAR}x{TINGGI}+{x}+{y}")

        self.label = ctk.CTkLabel(self, text="", fg_color=BG_HEX)
        self.label.pack(fill="both", expand=True)
        self.bind("<Button-1>", self.tutup)        # klik di mana saja = lewati

        self.mulai = time.perf_counter()
        self._frame()

    def _perbarui_progress(self, ms):
        """Tentukan kemajuan loading bar setelah bagian intro selesai."""
        if ms < INTRO_MS:
            return

        if self.tugas:                             # jalankan satu tugas nyata per frame
            tugas = self.tugas.pop(0)
            try:
                tugas()
            except Exception as e:
                print(f"Tugas loading gagal: {e}")
            self.tugas_selesai += 1

        target = self.tugas_selesai / self.jumlah_tugas if self.jumlah_tugas else 1.0
        self.progress = min(target, self.progress + LAJU_BAR)

        if self.progress >= 1.0 and self.waktu_tutup is None:
            self.waktu_tutup = ms + JEDA_AKHIR_MS

    def _frame(self):
        if self.ditutup:
            return
        try:
            ms = int((time.perf_counter() - self.mulai) * 1000)
            self._perbarui_progress(ms)

            gambar = render(state_at(ms, self.progress)).resize((LEBAR, TINGGI), Image.NEAREST)
            self.foto = ctk.CTkImage(light_image=gambar, dark_image=gambar, size=(LEBAR, TINGGI))
            self.label.configure(image=self.foto)

            if self.waktu_tutup is not None and ms >= self.waktu_tutup:
                self.tutup()
                return
        except Exception as e:                     # animasi gagal tidak boleh menahan aplikasi
            print(f"Splash dihentikan: {e}")
            self.tutup()
            return

        self.job = self.after(FRAME_MS, self._frame)

    def tutup(self, event=None):
        if self.ditutup:
            return
        self.ditutup = True
        if self.job is not None:
            try:
                self.after_cancel(self.job)
            except Exception:
                pass
        self.destroy()