# File: visualize_log.py
import pandas as pd
import matplotlib.pyplot as plt

CSV_FILE = 'sensor_log.csv'

try:
    df = pd.read_csv(CSV_FILE)
    print(f"Successfully loaded {len(df)} data points from {CSV_FILE}")

    df['time'] = df['timestamp'] - df['timestamp'].iloc[0]

    # Create 3 subplots instead of 4
    fig, axs = plt.subplots(3, 1, figsize=(12, 12), sharex=True)
    fig.suptitle('Rover Sensor Data Log', fontsize=16)

    # Plot Temperature
    axs[0].plot(df['time'], df['temperature'], color='red', label='Temperature (C)')
    axs[0].set_ylabel('Temperature (C)')
    axs[0].legend()
    axs[0].grid(True)

    # Plot Distance
    axs[1].plot(df['time'], df['distance'], color='blue', label='Distance (cm)')
    axs[1].set_ylabel('Distance (cm)')
    axs[1].legend()
    axs[1].grid(True)

    # Plot Accelerometer
    axs[2].plot(df['time'], df['accel_x'], label='Accel X')
    axs[2].plot(df['time'], df['accel_y'], label='Accel Y')
    axs[2].plot(df['time'], df['accel_z'], label='Accel Z')
    axs[2].set_ylabel('Acceleration (m/s)')
    axs[2].set_xlabel('Time (seconds)')
    axs[2].legend()
    axs[2].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

except FileNotFoundError:
    print(f"Error: Could not find the file '{CSV_FILE}'. Please run the rover app to generate it first.")
except Exception as e:
    print(f"An error occurred: {e}")
