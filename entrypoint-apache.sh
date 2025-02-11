#!/bin/sh
set -e

echo "Starting OpenVPN for Apache..."
openvpn --config /etc/openvpn/config.ovpn --auth-user-pass /etc/openvpn/credentials.txt --daemon

echo "Waiting for VPN connection..."
sleep 20

echo "Starting Apache server..."
exec httpd -D FOREGROUND
