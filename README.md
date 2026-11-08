# Inventaris Lab — Proyek Keamanan Aplikasi

Aplikasi inventaris sederhana berbasis Flask untuk demonstrasi autentikasi, otorisasi berbasis peran (RBAC), password hashing, container hardening, dan pengujian keamanan.

## 1. Peran pengguna

| Peran | Melihat barang | Menambah/mengubah barang | Menghapus barang | Mengelola pengguna |
|---|---:|---:|---:|---:|
| Admin | Ya | Ya | Ya | Ya |
| Staff | Ya | Ya | Tidak | Tidak |
| Viewer | Ya | Tidak | Tidak | Tidak |

## 2. Teknologi

- Python 3.12
- Flask
- SQLite
- Werkzeug `scrypt` untuk password hashing
- Docker / Docker Compose
- pytest, Trivy, Syft, Lynis (alat pemeriksaan eksternal)

## 3. Menjalankan secara lokal

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

pip install -r requirements.txt
# Linux/macOS:
export SECRET_KEY="ganti-dengan-random-secret-yang-panjang"
export DATABASE_PATH="./data/inventory.db"
export SEED_DEMO_USERS="1"
# Windows PowerShell:
# $env:SECRET_KEY="ganti-dengan-random-secret-yang-panjang"
# $env:DATABASE_PATH="./data/inventory.db"
# $env:SEED_DEMO_USERS="1"

python app.py
```

Aplikasi berjalan di `http://127.0.0.1:5000`.

### Akun demo (khusus lokal)

| Peran | Username | Password |
|---|---|---|
| Admin | `admin` | `Admin-Demo-2026!` |
| Staff | `staff` | `Staff-Demo-2026!` |
| Viewer | `viewer` | `Viewer-Demo-2026!` |

Ganti seluruh kredensial demo sebelum penggunaan nyata. Jangan gunakan data pengguna asli untuk demonstrasi.

## 4. Endpoint API

Semua endpoint selain `/health` dan `/api/login` memerlukan sesi login.

| Method | Endpoint | Izin |
|---|---|---|
| GET | `/health` | Publik |
| POST | `/api/login` | Publik |
| POST | `/api/logout` | Pengguna login |
| GET | `/api/items` | Admin, Staff, Viewer |
| POST | `/api/items` | Admin, Staff |
| PATCH | `/api/items/<id>` | Admin, Staff |
| DELETE | `/api/items/<id>` | Admin |
| GET | `/api/users` | Admin |
| POST | `/api/users` | Admin |

Contoh login menggunakan `curl`:

```bash
curl -i -c cookies.txt -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"Admin-Demo-2026!"}' \
  http://127.0.0.1:5000/api/login

curl -b cookies.txt http://127.0.0.1:5000/api/items
```

## 5. Pengujian

```bash
pip install -r requirements-dev.txt
pytest -v
```

Pengujian otomatis memeriksa akses yang diizinkan dan ditolak untuk setiap peran. Hasil aktual simpan ke `security/access-tests.md`.

## 6. Menjalankan dengan Docker

```bash
docker compose build
docker compose up -d
```

Compose sengaja tidak memiliki `ports:`. Aplikasi hanya dapat diakses dari jaringan internal Docker. Untuk demo, jalankan perintah curl dari container atau tambahkan reverse proxy yang sudah diamankan dan hanya bind ke localhost sesuai kebutuhan lab.

```bash
docker compose exec app python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8000/health').read().decode())"
docker compose down
```

## 7. Catatan penting

- `SECRET_KEY` wajib diganti dan disimpan sebagai secret, bukan di-commit.
- Akun demo hanya untuk pengujian lokal.
- File database berada di volume `inventory_data`.
- Container berjalan sebagai UID non-root, filesystem read-only, tanpa Linux capabilities, dan `no-new-privileges`.
- Hasil Trivy/Lynis/Syft harus dijalankan pada lingkungan aktual. Jangan mengisi hasil scan berdasarkan perkiraan.
- Script hardening VM mengubah konfigurasi SSH. Pastikan public key sudah terpasang dan akses konsol/akses pemulihan tersedia sebelum menjalankannya.
