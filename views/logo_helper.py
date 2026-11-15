import os

import customtkinter as ctk
from PIL import Image

FOLDER_ASET = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
FILE_LOGO = os.path.join(FOLDER_ASET, "logo_kopiloka.png")   # logo asli 75x80 piksel
FILE_IKON = os.path.join(FOLDER_ASET, "kopiloka.ico")


def muat_logo(skala=1):
    """
    CTkImage logo Kopiloka. skala = kelipatan BULAT dari ukuran asli 75x80 piksel
    (1 -> 75x80, 2 -> 150x160, 3 -> 225x240) supaya pixel art tetap tajam.
    """
    gambar = Image.open(FILE_LOGO)
    ukuran = (gambar.width * skala, gambar.height * skala)
    gambar = gambar.resize(ukuran, Image.NEAREST)
    return ctk.CTkImage(light_image=gambar, dark_image=gambar, size=ukuran)


def pasang_logo(master, skala=1, **opsi_pack):
    """
    Membuat label logo di `master` lalu langsung memasangnya dengan pack(**opsi_pack).
    Mengembalikan label-nya, atau None jika logo gagal dimuat (aplikasi tetap berjalan).
    """
    try:
        label = ctk.CTkLabel(master, text="", image=muat_logo(skala))
        label.pack(**opsi_pack)
        return label
    except Exception as e:
        print(f"Logo tidak dimuat: {e}")
        return None


def pasang_ikon(jendela):
    """
    Memasang ikon Kopiloka di title bar dan taskbar (khusus Windows, format .ico).
    Dijalankan sedikit tertunda karena CustomTkinter memasang ikon bawaannya sekitar 200 ms
    setelah window dibuat, dan ikon bawaan itu akan menimpa ikon kita kalau dipasang lebih awal.
    """
    if not os.path.exists(FILE_IKON):
        print(f"Ikon tidak ditemukan: {FILE_IKON}")
        return

    def _terapkan():
        try:
            jendela.iconbitmap(FILE_IKON)
        except Exception as e:
            print(f"Ikon tidak dipasang: {e}")

    jendela.after(300, _terapkan)