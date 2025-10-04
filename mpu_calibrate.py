# File: mpu_calibrate.py
import time
import board
import adafruit_mpu6050
from adafruit_bus_device import i2c_device

# (Use the same MPU6050_initializer_bypass function from mpu_test.py)
def MPU6050_initializer_bypass(i2c_bus, address=0x68):
    device = i2c_device.I2CDevice(i2c_bus, address)
    mpu = adafruit_mpu6050.MPU6050.__new__(adafruit_mpu6050.MPU6050)
    mpu.i2c_device = device
    mpu._gyro_range, mpu._accel_range = 0, 0
    mpu.gyro_range, mpu.accelerometer_range = 1, 0
    return mpu

print("Starting MPU6050 calibration. Keep the rover perfectly still...")
try:
    i2c = board.I2C()
    mpu = MPU6050_initializer_bypass(i2c)
    
    ax_list, ay_list, az_list = [], [], []
    gx_list, gy_list, gz_list = [], [], []

    # Take 200 readings
    for _ in range(200):
        accel = mpu.acceleration
        gyro = mpu.gyro
        ax_list.append(accel[0]); ay_list.append(accel[1]); az_list.append(accel[2])
        gx_list.append(gyro[0]); gy_list.append(gyro[1]); gz_list.append(gyro[2])
        time.sleep(0.01)

    # Calculate the average bias
    ax_bias = sum(ax_list) / len(ax_list)
    ay_bias = sum(ay_list) / len(ay_list)
    # The Z-axis for acceleration should read ~9.8 m/s^2 due to gravity, so we bias it against that
    az_bias = (sum(az_list) / len(az_list)) - 9.8 
    gx_bias = sum(gx_list) / len(gx_list)
    gy_bias = sum(gy_list) / len(gy_list)
    gz_bias = sum(gz_list) / len(gz_list)

    print("\nCalibration Complete. Here are your bias values:")
    print(f"ax_bias = {ax_bias:.4f}")
    print(f"ay_bias = {ay_bias:.4f}")
    print(f"az_bias = {az_bias:.4f}")
    print(f"gx_bias = {gx_bias:.4f}")
    print(f"gy_bias = {gy_bias:.4f}")
    print(f"gz_bias = {gz_bias:.4f}")
    print("\nCopy these values into your main sensor.py file.")

except Exception as e:
    print(f"Calibration failed. Error: {e}")
