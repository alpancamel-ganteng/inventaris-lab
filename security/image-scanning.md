# Image Vulnerability Scan dan SBOM

Pemindaian harus dilakukan pada mesin yang memiliki Docker dan Trivy. Simpan output asli; jangan mengarang hasil scan.

## 1. Baseline sebelum perbaikan

Untuk menghasilkan baseline yang bisa dibandingkan, build image awal dari Dockerfile baseline yang sengaja tidak menerapkan hardening runtime:

```bash
docker build -f security/before/Dockerfile -t inventaris-lab:before .
trivy image --severity CRITICAL,HIGH,MEDIUM inventaris-lab:before \
  --format table | tee security/image-scan-before.txt
```

## 2. Image setelah perbaikan

```bash
docker compose build --no-cache
trivy image --severity CRITICAL,HIGH,MEDIUM inventaris-lab:sec-0.2 \
  --format table | tee security/image-scan-after.txt
```

Periksa khusus temuan `CRITICAL`. Jika masih ada, perbarui base image/dependency, build ulang, lalu scan ulang. Target tugas: tidak ada kerentanan CRITICAL pada image akhir.

## 3. SBOM CycloneDX

```bash
syft inventaris-lab:sec-0.2 -o cyclonedx-json=sbom.cdx.json
```

SBOM harus dibuat dari image akhir yang benar-benar dibangun, bukan hanya daftar perkiraan dependency.

## 4. Catatan hasil

Isi tanggal, versi Docker/Trivy/Syft, nama image, jumlah temuan per severity, dan tindakan perbaikan. Simpan output mentah di repository.

### Hasil Pemindaian Aktual
Tanggal: 8 November 2026

| Keterangan | Baseline | Final |
|---|---:|---:|
| Image | inventaris-lab:before | inventaris-lab:sec-0.2 |
| Total | 1433 | 9 |
| CRITICAL | 31 | 0 |
| HIGH | 438 | 0 |
| MEDIUM | 964 | 9 |

### Tindakan Perbaikan
- Memperbarui paket pada image Docker.
- Melakukan build ulang image final.
- Melakukan pemindaian ulang menggunakan Trivy.
- Membuat SBOM format CycloneDX menggunakan Syft.

### Hasil
Image final tidak memiliki temuan CRITICAL maupun HIGH.
SBOM final dibuat dari image inventaris-lab:sec-0.2.