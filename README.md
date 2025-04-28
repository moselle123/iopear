# Raspberry Pi Based Plant Monitoring Web Application 🪴

## Project Overview
This project is a **smart plant monitoring and control system** built for the Raspberry Pi 3B+.
It monitors environmental data from I2C sensors and controls actuators via relays, all managed through a web interface.

The system uses:
- **Flask** (Python) backend
- **MongoDB** database
- **Vue.js** frontend
- **Docker** for containerization

The user can view live sensor data, configure settings and automate actions via the web application.

---

## Requirements

### Hardware
- Raspberry Pi 3B+ (or compatible Pi)
- MicroSD card (16GB or higher recommended)
- Internet connection (Preferably Ethernet for initial Docker downloads)
- Environmental sensors:
1. SHT31 - Temperature + Humidity
2. Adadfruit Stemma Soil Moisture Sensor - Soil Moisture + Soil Temperature
3. TSL2561 - Light Intensity
4. BMP280 - Barometric Pressure
5. SCD40 - CO2
- 1 or more relays for controlling actuators
- Actuators (e.g., water pumps, lights)

### Operating System
- Raspberry Pi OS Lite

### Software
- Docker
- Docker Compose
- Git

---

## Hardware Setup (Wiring Instructions)

### I2C Sensors
| Sensor Pin | Raspberry Pi Pin |
|:-----------|:-----------------|
| SDA        | GPIO2 (Pin 3)     |
| SCL        | GPIO3 (Pin 5)     |
| GND        | Ground (Any GND)  |
| VCC        | 3.3V or 5V (depends on sensor specs) |

Make sure to **enable I2C** on the Raspberry Pi:
```bash
sudo raspi-config
# Interface Options → I2C → Enable
```

### Relays / Actuators
| Relay Pin  | Raspberry Pi Pin  |
|:-----------|:------------------|
| IN1        | GPIO17 (example)   |
| IN2        | GPIO27 (example)   |
| GND        | Ground (Any GND)   |
| VCC        | 5V                 |

> **Important:** If your actuators need higher current, use a separate power supply to avoid damaging the Pi.

---

## Installation Instructions

1. **Install Docker and Docker Compose** on the Raspberry Pi:

```bash
curl -sSL https://get.docker.com | sh
sudo usermod -aG docker pi
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt install -y python3 python3-pip
sudo pip3 install docker-compose
```

2. **Clone the Repository**:

```bash
git clone https://campus.cs.le.ac.uk/gitlab/ug_project/24-25/mwpc1.git
cd mwpc1
```

3. **Build Docker Containers**:

```bash
docker compose -f docker-compose.dev.yml build
```

4. **Make the Startup Script Executable**:

```bash
chmod +x startup_script.sh
```

5. **Set Startup Script to Run on Boot**:

- Add `@reboot /home/pi/mwpc1/startup_script.sh` to the crontab:

```bash
crontab -e
```

At the bottom, add:
```bash
@reboot /home/pi/mwpc1/startup_script.sh
```

6. **Reboot the Raspberry Pi**:

```bash
sudo reboot
```

The application will automatically start running after reboot.

---

## Running the Application Manually

If you don't want to reboot, you can also manually start it:

```bash
./startup_script.sh
```

This will launch the Docker containers for the backend, frontend, and MongoDB.

---

## Third-party Software Used

- [Flask](https://flask.palletsprojects.com/) (Python web framework)
- [Vue.js](https://vuejs.org/) (Frontend framework)
- [MongoDB](https://www.mongodb.com/) (Database)
- [Adafruit CircuitPython](https://circuitpython.readthedocs.io/) (Sensor control libraries)
- [Docker](https://www.docker.com/) (Containerization)
- [Docker Compose](https://docs.docker.com/compose/) (Multi-container orchestration)

---

## Notes

- Ensure I2C is enabled on the Raspberry Pi before running the system.
- GPIO pins used for relays must be properly set up and sourced with correct voltage levels.
- MongoDB container stores data persistently unless containers are forcefully removed.
- The frontend Vue.js application is served through the Flask backend proxy.

