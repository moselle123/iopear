#!/bin/bash

export PATH=$PATH:/usr/local/bin

echo "🔄 Starting ioPear Setup..."

cd "$(dirname "$0")" || { echo "❌ Error: Could not navigate to project folder!"; exit 1; }

echo "🌐 Checking network status..."
sleep 5
if ! ip -4 addr show wlan0 | grep -q "inet "; then
    echo "❌ No network detected! Starting captive portal..."

    echo "🚀 Starting Captive Portal..."
    docker compose -f docker-compose.dev.yml up -d captive_portal

    while ! ip -4 addr show wlan0 | grep -q "inet "; do
        echo "🔄 Waiting for network connection..."
        sleep 10
    done

    echo "✅ Network connected! Stopping Captive Portal..."
    docker stop captive_portal_container
    docker rm captive_portal_container

    echo "🚀 Starting Main Application..."
    docker compose -f docker-compose.dev.yml up -d
else
    echo "✅ Network detected! Starting Main Application..."
    docker compose -f docker-compose.dev.yml up -d
fi

echo "✅ Setup complete!"