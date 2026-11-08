# AI Log

## Penanda tugas
- Tugas Pekan 3: `sec-0.1`
- Tugas Pekan 6: `sec-0.2`

## Bantuan AI
AI digunakan untuk membantu menyusun kerangka proyek, dokumentasi aset, DFD, STRIDE, risk register, matriks akses, dan contoh konfigurasi hardening.

## Verifikasi manusia yang wajib dilakukan
- [ ] Menjalankan aplikasi dan memeriksa endpoint.
- [ ] Menjalankan `pytest -v` dan menyimpan hasil aktual.
- [ ] Memastikan hash password menggunakan scrypt melalui demonstrasi.
- [ ] Menjalankan script hardening pada VM lab setelah memastikan akses pemulihan.
- [ ] Menjalankan Lynis dan mencatat indeks aktual.
- [ ] Build image Docker final.
- [ ] Menjalankan Trivy sebelum dan sesudah hardening dan menyimpan hasil aktual.
- [ ] Membuat SBOM final dari image dengan Syft.
- [ ] Memastikan tidak ada temuan CRITICAL pada image final.
- [ ] Menghubungkan setiap kontrol ke risiko pada `security/risk-register.md`.

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
