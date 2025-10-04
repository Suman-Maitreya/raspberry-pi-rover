# File: mpu_test.py (with safe reset)
import time
import board
import adafruit_mpu6050
from adafruit_bus_device import i2c_device

def MPU6050_initializer_bypass(i2c_bus, address=0x68):
    device = i2c_device.I2CDevice(i2c_bus, address)
    mpu = adafruit_mpu6050.MPU6050.__new__(adafruit_mpu6050.MPU6050)
    mpu.i2c_device = device
    mpu._gyro_range, mpu._accel_range = 0, 0
    
    # --- ADDED RESET ATTEMPT ---
    try:
        print("Attempting to reset the sensor...")
        mpu.reset()
        print("Sensor reset.")
    except Exception as e:
        print(f"Could not reset the sensor, but continuing anyway. Error: {e}")
    # --- END OF ADDED CODE ---

    mpu.gyro_range, mpu.accelerometer_range = 1, 0
    return mpu

try:
    i2c = board.I2C()
    mpu = MPU6050_initializer_bypass(i2c)
    print("MPU6050 Connected Successfully!")
    print("Reading data for 5 seconds...")
    for _ in range(10):
        accel = mpu.acceleration
        gyro = mpu.gyro
        print(f"Accel: X={accel[0]:.2f}, Y={accel[1]:.2f}, Z={accel[2]:.2f} | Gyro: X={gyro[0]:.2f}, Y={gyro[1]:.2f}, Z={gyro[2]:.2f}")
        time.sleep(0.5)
except Exception as e:
    print(f"Failed to connect or read from MPU6050. Error: {e}")
