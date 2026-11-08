#!/usr/bin/env bash
set -euo pipefail

# Jalankan hanya setelah public key SSH pengguna admin terpasang dan diuji.
if [[ "$(id -u)" -ne 0 ]]; then
  echo "Jalankan dengan sudo/root."
  exit 1
fi

ADMIN_USER="${SUDO_USER:-}"
if [[ -z "$ADMIN_USER" || ! -s "/home/$ADMIN_USER/.ssh/authorized_keys" ]]; then
  echo "ABORT: authorized_keys untuk pengguna admin belum ditemukan."
  echo "Pasang dan uji SSH key terlebih dahulu agar tidak terkunci dari VM."
  exit 1
fi

BACKUP="/root/ssh-config-backup-$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP"
cp -a /etc/ssh/sshd_config "$BACKUP/sshd_config"

apt-get update
apt-get install -y openssh-server ufw lynis

cat > /etc/ssh/sshd_config.d/99-security-hardening.conf <<'EOF'
PubkeyAuthentication yes
PasswordAuthentication no
KbdInteractiveAuthentication no
PermitRootLogin no
PermitEmptyPasswords no
MaxAuthTries 3
X11Forwarding no
AllowAgentForwarding no
AllowTcpForwarding no
EOF

sshd -t
systemctl reload ssh || systemctl reload sshd
ufw allow OpenSSH
ufw --force enable

echo "Konfigurasi SSH telah diterapkan. Buka sesi SSH kedua dan uji key login sebelum menutup sesi saat ini."
echo "Backup konfigurasi: $BACKUP"
echo "Jalankan: sudo lynis audit system"
