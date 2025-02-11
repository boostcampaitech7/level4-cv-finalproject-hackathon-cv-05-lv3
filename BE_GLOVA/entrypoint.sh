#!/bin/bash
set -e

echo "Setting up SSH config for Server2..."
mkdir -p /root/.ssh
cat <<'EOF' > /root/.ssh/config
Host Server2
    HostName 10.28.224.35
    User root
    Port 30699
    IdentityFile /etc/ssh/beomjoismoving.pem
EOF
chmod 600 /root/.ssh/config

echo "Starting OpenVPN..."
# credentials.txt를 이용해 OpenVPN 실행
openvpn --config /etc/openvpn/config.ovpn --auth-user-pass /etc/openvpn/credentials.txt &
VPN_PID=$!

echo "Waiting for VPN connection..."
sleep 20

echo "Testing SSH connectivity to Server2..."
# SSH 접속 시 "Server2" 별칭 사용
ssh -o StrictHostKeyChecking=no Server2 "echo 'SSH Tunnel is working!'"

echo "Establishing additional SSH tunnel for server doubling..."
# 추가 포트 포워딩 터널 실행 (백그라운드에서 실행)
ssh -N -i /etc/ssh/beomjoismoving.pem \
    -L 3307:10.28.224.109:3306 \
    -L 5433:10.28.224.131:5432 \
    root@10.28.224.35 -p 30699 &
SSH_TUNNEL_PID=$!
echo "Additional SSH tunnel established with PID: $SSH_TUNNEL_PID"

# 컨테이너가 종료되지 않도록 무한 루프를 실행
echo "Container is kept alive. Press Ctrl+C to exit."
exec "$@"
