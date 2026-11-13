import hashlib


def hash_password(password):
    """Mengubah password teks biasa menjadi hash SHA-256 (satu arah, 64 karakter heksadesimal)."""
    return hashlib.sha256(password.encode("utf-8")).hexdigest()
