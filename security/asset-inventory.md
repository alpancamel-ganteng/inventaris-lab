# Asset Inventory

## Deskripsi produk
Inventaris Lab adalah aplikasi web internal untuk mencatat barang laboratorium. Aplikasi menggunakan Flask, SQLite, dan autentikasi berbasis sesi.

| ID | Aset/komponen | Jenis | Data yang diproses | Perlindungan |
|---|---|---|---|---|
| A-01 | Akun pengguna | Data identitas | Username, role, password hash | Scrypt hash, RBAC |
| A-02 | Database SQLite | Data | Data barang dan akun | Volume Docker, akses UID aplikasi |
| A-03 | Password hash | Data rahasia turunan | Hash scrypt | Tidak pernah mengembalikan hash melalui API |
| A-04 | Session cookie | Kredensial sesi | ID pengguna dalam sesi bertanda tangan | HttpOnly, SameSite, Secure saat HTTPS |
| A-05 | API aplikasi | Komponen | Permintaan dan respons inventaris | Autentikasi dan otorisasi |
| A-06 | Docker image | Artefak perangkat lunak | Runtime dan dependency | Image scan, versi dependency dipatok |
| A-07 | VM Linux | Infrastruktur | OS, SSH, log | SSH key-only, root login ditolak, firewall |
| A-08 | Secret key | Rahasia konfigurasi | Kunci penandatanganan sesi | Environment secret, tidak di-commit |

## Data yang dilindungi secara kriptografi
- Password tidak disimpan dalam bentuk plaintext; aplikasi menyimpan hash `scrypt`.
- Session cookie ditandatangani oleh Flask menggunakan `SECRET_KEY`.
- Untuk penggunaan produksi, seluruh trafik harus melewati HTTPS dan `COOKIE_SECURE=1`.
- SQLite tidak dienkripsi pada contoh ini. Jika data inventaris bersifat sensitif, gunakan enkripsi disk/volume dan kontrol akses backup.
