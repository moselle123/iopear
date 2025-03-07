#!/bin/bash

echo "Starting ioPear Setup..."

cd /mwpc1 || { echo "Error: Project folder /mwpc1 not found!"; exit 1; }

echo "Enabling I2C..."
sudo raspi-config nonint do_i2c 0

echo "Checking network status..."
if ! ping -q -c 1 -W 1 8.8.8.8 >/dev/null; then
	echo "No network detected! Starting captive portal..."

	sudo systemctl start hostapd
	sudo systemctl start dnsmasq

	docker-compose -f docker-compose.dev.yml up -d captive_portal

	exit 0
fi

echo "Network detected... Starting main app..."

sudo systemctl start docker

docker-compose -f docker-compose.dev.yml up -d

echo "Setup complete!"
