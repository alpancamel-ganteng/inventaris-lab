# AI Log

## Penanda tugas
- Tugas Pekan 3: `sec-0.1`
- Tugas Pekan 6: `sec-0.2`

## Bantuan AI
AI digunakan untuk membantu menyusun kerangka proyek, dokumentasi aset, DFD, STRIDE, risk register, matriks akses, dan contoh konfigurasi hardening.

## Verifikasi manusia dan hasil pengerjaan

- [x] Menjalankan aplikasi dan memeriksa endpoint.
- [ ] Menjalankan `pytest -v` dan menyimpan hasil aktual.
- [x] Memastikan password menggunakan hashing scrypt.
- [x] Melakukan hardening pada Ubuntu Server.
- [x] Menjalankan Lynis dan memperoleh Hardening Index 70.
- [x] Build image Docker final.
- [x] Menjalankan Trivy sebelum dan sesudah hardening serta menyimpan hasil scan.
- [x] Membuat SBOM final dengan format CycloneDX menggunakan Trivy.
- [x] Memastikan tidak ada temuan CRITICAL pada image final.
- [ ] Memastikan setiap kontrol keamanan terhubung dengan Risk ID pada `security/risk-register.md`.

## Catatan integritas
File bukti scan dan indeks Lynis belum diisi karena hasilnya harus berasal dari lingkungan eksekusi aktual. Jangan mengklaim pengujian berhasil sebelum menjalankannya.


HASIL HARDENING DAN SECURITY SCAN



1. Ubuntu Server

- Lynis Hardening Index: 70

- UFW: Active

- SSH: Key-based authentication

- Root SSH login: Disabled

- Fail2ban: Active

- GRUB: Password protection enabled



2. Docker Security

- Docker container berjalan sebagai non-root user

- UID: 10001

- GID: 10001

- Container status: Healthy



3. Trivy Scan

- UNKNOWN: 0

- LOW: 2

- MEDIUM: 9

- HIGH: 0

- CRITICAL: 0



4. Software Bill of Materials

- Format: CycloneDX

- File: sbom.cdx.json

- Status: Successfully generated

5. GRUB: Password Protection Enabled
