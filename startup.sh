echo "🔄 Checking network status..."
sleep 5

if ip -4 addr show wlan0 | grep -q "inet 192\.168\|inet 10\|inet 172"; then
	if ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
		echo "✅ Network detected! Stopping Captive Portal..."
		sudo systemctl stop hostapd
		sudo systemctl stop dnsmasq
		sudo systemctl stop captive_portal
		echo "🚀 Starting Main Application..."
		docker compose -f docker-compose.dev.yml up -d
		exit 0
	fi
fi

echo "❌ No internet detected! Enabling Captive Portal..."
sudo systemctl restart hostapd
sudo systemctl restart dnsmasq

source /home/admin/mwpc1/captive_portal/venv/bin/activate
python /home/admin/mwpc1/captive_portal/captive_portal.py &

while true; do
	if ip -4 addr show wlan0 | grep -q "inet 192\.168\|inet 10\|inet 172"; then
		if ping -c 1 -W 2 8.8.8.8 >/dev/null 2>&1; then
			echo "✅ Network connected! Stopping Captive Portal..."
			sudo systemctl stop hostapd
			sudo systemctl stop dnsmasq
			sudo systemctl stop captive_portal
			echo "🚀 Starting Main Application..."
			docker compose -f docker-compose.dev.yml up -d
			exit 0
		fi
	fi
	echo "🔄 Waiting for network connection..."
	sleep 10
done
