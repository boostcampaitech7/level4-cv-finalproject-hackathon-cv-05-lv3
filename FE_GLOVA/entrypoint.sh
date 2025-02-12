#!/bin/bash
set -e

echo "Starting OpenVPN for Frontend..."
openvpn --config /etc/openvpn/config.ovpn --auth-user-pass /etc/openvpn/credentials.txt &
VPN_PID=$!

echo "Waiting for VPN connection..."
sleep 20

echo "Starting Frontend server..."
exec npm run dev
