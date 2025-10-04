# Raspberry Pi 6WD Rover Controller

A 6-wheeled rover controlled by a Raspberry Pi via a real-time web interface, featuring manual and autonomous line-following modes.

## ?? Features
- **Real-Time Web Interface:** A futuristic, mobile-friendly UI built with Flask-SocketIO.
- **Manual Control:** Full control over the rover's movement with variable speed.
- **Autonomous Mode:** A line-follower mode using two downward-facing IR sensors.
- **Live Sensor Telemetry:** Displays data from DHT11, HC-SR04, and IR sensors.

## ??? Hardware
- Raspberry Pi
- 6x DC Motors & 6WD chassis
- 3x L298N Motor Drivers
- 12V Battery & Buck Converter
- 2x IR Sensors
- 1x HC-SR04 Ultrasonic Sensor
- 1x DHT11 Sensor

## ?? Setup
1. Clone the repository.
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## ?? Usage
Run the application (may require sudo for GPIO access):
```bash
sudo python app.py
