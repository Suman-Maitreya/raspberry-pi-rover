# File: test_ultrasonic.py
import lgpio
import time

ULTRASONIC_TRIGGER = 23
ULTRASONIC_ECHO = 24

try:
    h = lgpio.gpiochip_open(0)
    lgpio.gpio_claim_output(h, ULTRASONIC_TRIGGER)
    lgpio.gpio_claim_input(h, ULTRASONIC_ECHO)
    print("Testing Ultrasonic Sensor. Press Ctrl+C to stop.")
    while True:
        lgpio.gpio_write(h, ULTRASONIC_TRIGGER, 1)
        time.sleep(0.00001)
        lgpio.gpio_write(h, ULTRASONIC_TRIGGER, 0)
        
        start_time, stop_time = time.time(), time.time()
        
        timeout_start = time.time()
        while lgpio.gpio_read(h, ULTRASONIC_ECHO) == 0:
            start_time = time.time()
            if start_time - timeout_start > 0.1: 
                print("Error: Timed out waiting for echo pulse to start. Check wiring.")
                break
        else: # This block runs if the while loop completes without a break
            timeout_start = time.time()
            while lgpio.gpio_read(h, ULTRASONIC_ECHO) == 1:
                stop_time = time.time()
                if stop_time - timeout_start > 0.1: 
                    print("Error: Timed out waiting for echo pulse to end. Check wiring.")
                    break
            else:
                distance = ((stop_time - start_time) * 34300) / 2
                if distance > 0 and distance < 400:
                     print(f"Distance: {distance:.2f} cm")

        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nStopping test.")
finally:
    lgpio.gpiochip_close(h)
