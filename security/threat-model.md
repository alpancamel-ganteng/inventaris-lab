# Threat Model — STRIDE

| ID | Elemen DFD | STRIDE | Ancaman spesifik | Aset terdampak | Kontrol |
|---|---|---|---|---|---|
| T-01 | P-01 login | Spoofing | Penyerang mencoba login menggunakan password akun yang ditebak | A-01 | Scrypt, password minimum 12 karakter untuk akun baru, respons login generik |
| T-02 | B-01 cookie | Spoofing | Cookie sesi dicuri lalu dipakai untuk menyamar sebagai pengguna | A-04 | HttpOnly, SameSite, Secure saat HTTPS, sesi dibersihkan saat logout |
| T-03 | P-02 RBAC | Tampering | Viewer mengirim POST/PATCH/DELETE langsung ke API | A-05, A-02 | Pemeriksaan role di sisi server dan tes negatif |
| T-04 | P-01 input barang | Tampering | Input quantity negatif atau tipe data salah merusak konsistensi data | A-02 | Validasi tipe/rentang dan constraint database |
| T-05 | P-01 query | Tampering | Input dibuat untuk memanipulasi query SQL | A-02 | Parameterized SQL |
| T-06 | P-01 respons API | Repudiation | Pengguna menyangkal perubahan karena tidak ada audit trail | A-02 | Risiko tersisa: tambahkan audit log terpisah sebelum produksi |
| T-07 | P-01/API | Information Disclosure | Endpoint pengguna membocorkan password hash | A-01, A-03 | Query daftar pengguna hanya memilih id, username, role |
| T-08 | D-01 SQLite | Information Disclosure | Penyerang yang memperoleh file DB membaca data inventaris | A-02 | UID non-root, volume terbatas; enkripsi volume/backup menjadi pekerjaan lanjutan |
| T-09 | P-01 | Denial of Service | Request berulang menghabiskan worker aplikasi | A-05 | Batas worker/timeout; rate limiting dan reverse proxy WAF belum diterapkan |
| T-10 | Docker image | Elevation of Privilege | Proses aplikasi yang tereksploitasi mencoba memperoleh hak root/container host | A-06, A-07 | UID non-root, cap_drop ALL, no-new-privileges, read-only filesystem |
| T-11 | S-01 secret | Information Disclosure | SECRET_KEY masuk ke repository atau image | A-08, A-04 | Environment secret, .gitignore, tidak disimpan di source |
| T-12 | Docker network | Information Disclosure | Database atau port aplikasi terekspos ke jaringan host | A-02, A-05 | Tidak ada `ports:`; hanya `expose` pada jaringan internal |

## Catatan
Ancaman mengacu pada elemen DFD yang spesifik. Kontrol yang belum tersedia ditandai sebagai risiko tersisa dan tidak boleh diklaim sudah selesai.
