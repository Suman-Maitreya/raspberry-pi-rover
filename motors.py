# File: motors.py
import lgpio
import time

# --- GPIO Setup using lgpio ---
h = lgpio.gpiochip_open(0)

# --- Define Motor Pins ---
MOTOR_FL = {'ena': 21, 'in1': 17, 'in2': 18}
MOTOR_ML = {'ena': 22, 'in1': 27, 'in2': 25}
MOTOR_RL = {'ena': 12, 'in1': 5,  'in2': 6}
MOTOR_FR = {'ena': 13, 'in1': 16, 'in2': 26}
MOTOR_MR = {'ena': 19, 'in1': 7,  'in2': 8}
MOTOR_RR = {'ena': 20, 'in1': 11, 'in2': 9}

ALL_MOTORS = [MOTOR_FL, MOTOR_ML, MOTOR_RL, MOTOR_FR, MOTOR_MR, MOTOR_RR]
LEFT_MOTORS = [MOTOR_FL, MOTOR_ML, MOTOR_RL]
RIGHT_MOTORS = [MOTOR_FR, MOTOR_MR, MOTOR_RR]

ALL_PINS = [pin for motor in ALL_MOTORS for pin in motor.values()]
for pin in ALL_PINS:
    lgpio.gpio_claim_output(h, pin)

# --- Speed Control Variable ---
drive_speed = 80 # Default speed

def update_drive_speed(new_speed):
    """Updates the global drive speed, with safety checks."""
    global drive_speed
    try:
        speed_val = int(new_speed)
        if 30 <= speed_val <= 100:
            drive_speed = speed_val
            print(f"Speed updated to: {drive_speed}%")
        else:
            print(f"Invalid speed: {speed_val}. Must be between 30 and 100.")
    except ValueError:
        print("Invalid speed value received.")

def set_pwm_speed(speed):
    """Sets the PWM for all motors."""
    for motor in ALL_MOTORS:
        lgpio.tx_pwm(h, motor['ena'], 100, speed)

def forward():
    print(f"Moving forward at {drive_speed}%")
    for motor in LEFT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 1); lgpio.gpio_write(h, motor['in2'], 0)
    for motor in RIGHT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 1); lgpio.gpio_write(h, motor['in2'], 0)
    set_pwm_speed(drive_speed)

def backward():
    print(f"Moving backward at {drive_speed}%")
    for motor in LEFT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 0); lgpio.gpio_write(h, motor['in2'], 1)
    for motor in RIGHT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 0); lgpio.gpio_write(h, motor['in2'], 1)
    set_pwm_speed(drive_speed)

def left():
    print(f"Turning left at {drive_speed}%")
    for motor in LEFT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 0); lgpio.gpio_write(h, motor['in2'], 1)
    for motor in RIGHT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 1); lgpio.gpio_write(h, motor['in2'], 0)
    set_pwm_speed(drive_speed - 10) # Turn a bit slower

def right():
    print(f"Turning right at {drive_speed}%")
    for motor in LEFT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 1); lgpio.gpio_write(h, motor['in2'], 0)
    for motor in RIGHT_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 0); lgpio.gpio_write(h, motor['in2'], 1)
    set_pwm_speed(drive_speed - 10) # Turn a bit slower

def stop():
    print("Stopping")
    set_pwm_speed(0)
    for motor in ALL_MOTORS:
        lgpio.gpio_write(h, motor['in1'], 0); lgpio.gpio_write(h, motor['in2'], 0)

def cleanup():
    print("Cleaning up GPIO")
    stop()
    lgpio.gpiochip_close(h)
