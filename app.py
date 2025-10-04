# File: app.py
import time
from flask import Flask, render_template
from flask_socketio import SocketIO
import atexit
import sensor
import motors
import csv
import os

app = Flask(__name__)
socketio = SocketIO(app)

# --- THREADS AND STATE ---
sensor_thread = None
logging_thread = None
is_logging = False
CSV_FILE = 'sensor_log.csv'

def setup_csv():
    """Creates the CSV file and writes the header if it doesn't exist."""
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE) # Remove old file to match new header
    
    # Header without gyroscope
    header = ['timestamp', 'temperature', 'distance', 'accel_x', 'accel_y', 'accel_z']
    with open(CSV_FILE, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(header)

def sensor_background_thread():
    """Sends sensor data to the web interface."""
    while True:
        socketio.sleep(1)
        ir_data = sensor.get_ir_status()
        sensor_data = {
            'temp': sensor.get_temp(),
            'distance': sensor.get_distance(),
            'ir_1': ir_data['ir_1'],
            'ir_2': ir_data['ir_2'],
            'mpu': sensor.get_mpu9250()
        }
        socketio.emit('update_sensors', sensor_data)

def logging_thread():
    """Logs sensor data to CSV when active."""
    while True:
        if is_logging:
            mpu_data = sensor.get_mpu9250()
            # Data row without gyroscope
            row = [
                time.time(),
                sensor.get_temp(),
                sensor.get_distance(),
                mpu_data['ax'],
                mpu_data['ay'],
                mpu_data['az']
            ]
            with open(CSV_FILE, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(row)
            print(f"Logged data point")
            socketio.sleep(0.5)
        else:
            socketio.sleep(1)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    global sensor_thread
    if sensor_thread is None:
        sensor_thread = socketio.start_background_task(target=sensor_background_thread)
    print('Client connected')

@socketio.on('control_event')
def handle_control_event(json):
    command = json.get('data')
    if command == 'forward': motors.forward()
    elif command == 'backward': motors.backward()
    elif command == 'left': motors.left()
    elif command == 'right': motors.right()
    elif command == 'stop': motors.stop()

@socketio.on('toggle_logging')
def handle_toggle_logging():
    global is_logging
    is_logging = not is_logging
    print(f"Logging toggled: {'ACTIVE' if is_logging else 'INACTIVE'}")
    socketio.emit('logging_status', {'active': is_logging})

@socketio.on('set_speed')
def handle_set_speed(json):
    speed = json.get('speed')
    motors.update_drive_speed(speed)

@atexit.register
def cleanup_on_exit():
    print("Application shutting down, cleaning up GPIO...")
    motors.cleanup()
    sensor.cleanup()

if __name__ == '__main__':
    setup_csv()
    logging_thread = socketio.start_background_task(target=logging_thread)
    socketio.run(app, debug=True, host='0.0.0.0', port=5000, use_reloader=False)
