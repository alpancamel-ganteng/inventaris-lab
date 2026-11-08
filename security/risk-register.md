# Risk Register

Skala: kemungkinan (K) 1–5, dampak (D) 1–5, skor = K × D. Skor digunakan untuk mengurutkan prioritas, bukan pengganti alasan kualitatif.

| ID | Ancaman | Kemungkinan | Dampak | Skor | Alasan berdasarkan produk | Prioritas |
|---|---|---:|---:|---:|---|---|
| R-01 | Akses tidak sah akibat password lemah/tebakan (T-01) | 4 | 5 | 20 | Aplikasi internal dapat diakses banyak pengguna; akun demo dan password yang mudah ditebak berisiko bila tidak diganti | 1 |
| R-02 | Viewer melakukan perubahan langsung ke API (T-03) | 3 | 5 | 15 | API dapat dipanggil tanpa antarmuka browser; kontrol UI saja tidak cukup | 2 |
| R-03 | Kebocoran session cookie (T-02) | 3 | 5 | 15 | Cookie membawa identitas sesi; pencurian cookie dapat memberi akses sesuai role korban | 3 |
| R-04 | File SQLite disalin dari host/backup (T-08) | 3 | 4 | 12 | Database berada pada volume persisten; contoh belum mengenkripsi file database | 4 | 
**Status Implementasi: Berhasil**

- Hak akses file database: 600.
- Hak akses folder database: 700.
- Pemilik database dan folder: UID/GID 10001.
- Pengujian akses baca dan tulis database oleh aplikasi: Berhasil.

Pembatasan hak akses dilakukan untuk mencegah pengguna lain mengakses file database tanpa izin.
| R-05 | Container dieksploitasi dan memperoleh privilege tinggi (T-10) | 2 | 5 | 10 | Aplikasi memproses input jaringan; konfigurasi container yang longgar memperbesar dampak kompromi | 5 |
| R-06 | SQL injection (T-05) | 2 | 5 | 10 | Endpoint menerima input; query parameterized sudah mengurangi kemungkinan |
| R-07 | DoS melalui request berulang (T-09) | 3 | 3 | 9 | Worker aplikasi terbatas, tetapi belum ada rate limit |
| R-08 | Secret key terekspos (T-11) | 2 | 5 | 10 | Kunci yang bocor dapat memungkinkan pemalsuan cookie bertanda tangan |

## Lima risiko prioritas dan rencana kontrol

1. **R-01 — Password dan autentikasi (Tugas 2 / kontrol aplikasi).** Gunakan scrypt, password minimum 12 karakter saat membuat akun, jangan menyimpan plaintext, ganti akun demo, dan uji password salah.
2. **R-02 — Otorisasi RBAC (Tugas 2 / kontrol aplikasi).** Terapkan pemeriksaan role di server pada setiap endpoint; jalankan pengujian positif dan negatif untuk admin, staff, viewer.
3. **R-03 — Session cookie (Tugas 2 / kontrol aplikasi).** Aktifkan HTTPS di reverse proxy, `COOKIE_SECURE=1`, HttpOnly, SameSite, masa sesi terbatas, dan logout yang membersihkan sesi.
4. **R-04 — Database dan backup (Tugas 3 / hardening).** Batasi hak file/volume, akses hanya untuk UID aplikasi, enkripsi disk/backup pada host, dan uji pemulihan backup.
5. **R-05 — Container privilege (Tugas 3 / hardening).** Jalankan non-root, drop semua capability, no-new-privileges, filesystem read-only, tidak publish port, lalu scan image.

## Risiko tersisa
- Belum ada audit log append-only untuk perubahan inventaris.
- Belum ada rate limiting.
- SQLite belum dienkripsi pada level aplikasi.
- TLS harus disediakan oleh reverse proxy/ingress yang dikelola terpisah.
