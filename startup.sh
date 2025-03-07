#!/bin/bash

export PATH=$PATH:/usr/local/bin

echo "Starting ioPear Setup..."

cd "$(dirname "$0")" || { echo "Error: Could not navigate to project folder!"; exit 1; }

echo "Installing required packages..."
sudo apt update
sudo apt install -y hostapd dnsmasq iptables-persistent docker-compose


echo "Enabling I2C..."
sudo raspi-config nonint do_i2c 0


echo "Configuring Wi-Fi AP..."
if [ ! -f /etc/hostapd/hostapd.conf ]; then
    sudo bash -c 'cat > /etc/hostapd/hostapd.conf' <<EOF
interface=wlan0
driver=nl80211
ssid=ioPear_Setup
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=raspberry
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
EOF
fi

sudo sed -i 's|#DAEMON_CONF=""|DAEMON_CONF="/etc/hostapd/hostapd.conf"|' /etc/default/hostapd

echo "Configuring DHCP..."
if [ ! -f /etc/dnsmasq.conf ]; then
    sudo bash -c 'cat > /etc/dnsmasq.conf' <<EOF
interface=wlan0
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
address=/#/192.168.4.1
EOF
fi

echo "Enabling IP forwarding..."
sudo sed -i 's|#net.ipv4.ip_forward=1|net.ipv4.ip_forward=1|' /etc/sysctl.conf
sudo sysctl -p

echo "Restarting AP services..."
sudo systemctl stop hostapd dnsmasq
sleep 2
sudo systemctl start hostapd dnsmasq
sudo systemctl enable hostapd dnsmasq

echo "Checking network status..."
sleep 10

if ! ip -4 addr show wlan0 | grep -q "inet "; then
    echo "No network detected! Starting captive portal..."

    /usr/local/bin/docker-compose -f docker-compose.dev.yml up -d captive_portal

    exit 0
fi

echo "Network detected... Starting main app..."
sudo systemctl start docker
docker compose -f docker compose.dev.yml up -d

echo "Setup complete!"
