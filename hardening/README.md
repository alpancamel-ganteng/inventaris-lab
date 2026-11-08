# VM Hardening

Jalankan pada VM Ubuntu/Debian yang dikhususkan untuk lab.

1. Buat pengguna admin non-root.
2. Pasang public key pada `~/.ssh/authorized_keys`.
3. Buka sesi SSH baru dan pastikan login menggunakan key berhasil.
4. Pastikan akses konsol VM tersedia sebagai jalur pemulihan.
5. Jalankan `sudo bash hardening/harden_ubuntu.sh`.
6. Uji kembali login SSH menggunakan key.
7. Uji bahwa root SSH dan password SSH ditolak.
8. Jalankan `sudo lynis audit system`.

Bukti yang harus dikumpulkan:

```bash
sudo sshd -T | grep -E 'permitrootlogin|passwordauthentication|pubkeyauthentication'
sudo lynis audit system
```

Kondisi yang diharapkan:
- `permitrootlogin no`
- `passwordauthentication no`
- `pubkeyauthentication yes`
- Indeks Lynis minimal 70 (nilai aktual harus berasal dari hasil audit VM).

Jangan jalankan script pada server penting atau VM tanpa akses konsol/pemulihan.
