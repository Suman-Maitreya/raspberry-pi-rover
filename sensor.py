# File: sensor.py
import lgpio
import time
import board
import adafruit_dht
from mpu9250_jmdev.mpu_9250 import MPU9250 

# --- SENSOR INITIALIZATION ---
ULTRASONIC_TRIGGER = 23
ULTRASONIC_ECHO = 24
IR_PIN_1 = 14
IR_PIN_2 = 15
DHT_PIN = 4

h = lgpio.gpiochip_open(0)
lgpio.gpio_claim_output(h, ULTRASONIC_TRIGGER)
lgpio.gpio_claim_input(h, ULTRASONIC_ECHO)
lgpio.gpio_claim_input(h, IR_PIN_1)
lgpio.gpio_claim_input(h, IR_PIN_2)

mpu = MPU9250()
mpu.configure() 
dht_sensor = adafruit_dht.DHT11(getattr(board, f"D{DHT_PIN}"))

# --- SENSOR READING FUNCTIONS ---
def get_temp():
    try:
        temp = dht_sensor.temperature
        return round(temp, 1) if temp is not None else 0.0
    except RuntimeError:
        return 0.0

def get_distance():
    try:
        lgpio.gpio_write(h, ULTRASONIC_TRIGGER, 1); time.sleep(0.00001); lgpio.gpio_write(h, ULTRASONIC_TRIGGER, 0)
        start_time, stop_time = time.time(), time.time()
        timeout = time.time()
        while lgpio.gpio_read(h, ULTRASONIC_ECHO) == 0:
            start_time = time.time()
            if start_time - timeout > 0.1: return -1
        timeout = time.time()
        while lgpio.gpio_read(h, ULTRASONIC_ECHO) == 1:
            stop_time = time.time()
            if stop_time - timeout > 0.1: return -1
        return round(((stop_time - start_time) * 34300) / 2, 2)
    except Exception:
        return -1

def get_ir_status():
    try:
        ir1 = lgpio.gpio_read(h, IR_PIN_1) == 0
        ir2 = lgpio.gpio_read(h, IR_PIN_2) == 0
        return {'ir_1': ir1, 'ir_2': ir2}
    except Exception:
        return {'ir_1': False, 'ir_2': False}

def get_mpu9250():
    """Reads only the MPU9250 accelerometer."""
    try:
        accel = mpu.readAccelerometerMaster()
        return {
            'ax': round(accel[0], 2), 'ay': round(accel[1], 2), 'az': round(accel[2], 2)
        }
    except Exception as e:
        # print(f"MPU9250 Error: {e}")
        return {'ax': 0, 'ay': 0, 'az': 0}

def cleanup():
    lgpio.gpiochip_close(h)
