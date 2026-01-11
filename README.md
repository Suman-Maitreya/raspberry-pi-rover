# 🚜 MTR-1: 6-Wheel Multi-Terrain Research Rover
### An IoT-Enabled UGV for Uneven Terrain Analysis & Teleoperation

![Status](https://img.shields.io/badge/Status-Completed-success)
![Platform](https://img.shields.io/badge/Platform-Raspberry_Pi_4-C51A4A?logo=raspberry-pi)
![Language](https://img.shields.io/badge/Language-Python_3.9-blue?logo=python)
![Framework](https://img.shields.io/badge/Backend-Flask-green?logo=flask)
![Hardware](https://img.shields.io/badge/Drivers-L298N-orange)

---

## 📋 Table of Contents
1. [Project Abstract](#-project-abstract)
2. [Key Features](#-key-features)
3. [System Architecture](#-system-architecture)
4. [Hardware Components](#-hardware-components)
5. [Pinout & Circuitry](#-pinout--circuitry)
6. [Installation & Setup](#-installation--setup)
7. [Usage Guide](#-usage-guide)
8. [Project Structure](#-project-structure)
9. [Future Scope](#-future-roadmap-mobile-robotics)

---

## 📖 Project Abstract
The **MTR-1 (Multi-Terrain Rover)** is a six-wheeled Unmanned Ground Vehicle (UGV) engineered to study locomotion dynamics on non-standard surfaces. Addressing the limitations of standard 4-wheel chassis designs, this project utilizes a 6-wheel drive configuration to maximize traction and stability on gravel, inclines, and loose soil.

The rover is controlled via a low-latency **Flask-based web interface** hosted locally on the robot, allowing for Wi-Fi teleoperation. It integrates an **IMU (MPU-6050)** for real-time tilt monitoring and an **Ultrasonic Sensor (HC-SR04)** for obstacle proximity alerts, serving as a foundational platform for autonomous mobile robotics research.

---

## ✨ Key Features
* **6-Wheel Drive (6WD):** Superior grip and torque distribution compared to 4WD, allowing for zero-radius turns and climbing capabilities >15°.
* **Wi-Fi Teleoperation:** Custom-built Web UI (HTML5/AJAX) for controlling the rover from any smartphone or laptop on the same network.
* **Real-Time Telemetry:**
    * *Pitch/Roll Analysis:* Monitors chassis stability using the onboard Gyroscope/Accelerometer.
    * *Proximity Warning:* Detects frontal obstacles (<30cm) to prevent collisions.
* **Differential Steering:** Logic-based steering control (skid-steer) implemented in Python.

---

## 🧠 System Architecture

### The "Brain" (Raspberry Pi)
The Raspberry Pi acts as the central server. It runs a Python Flask application that listens for HTTP requests from the client (Web UI).

### The Data Flow
1.  **User Input:** User presses "Forward" on the Web UI.
2.  **Request:** JavaScript sends an asynchronous `POST` request to the Pi.
3.  **Processing:** Flask receives the request and triggers the GPIO pins.
4.  **Actuation:** L298N drivers receive the signal and power the 6 motors.
5.  **Feedback:** Sensors read environment data and update the Web UI via API calls.

---

## 🛠 Hardware Components

| Component | Model/Type | Quantity | Purpose |
| :--- | :--- | :--- | :--- |
| **SBC** | Raspberry Pi 4 Model B (4GB) | 1 | Main Controller & Web Server |
| **Motor Drivers** | L298N H-Bridge Module | 2 | Controls 3 motors each (Left/Right banks) |
| **Motors** | 12V High-Torque DC Gear Motors | 6 | 300 RPM High-Torque actuation |
| **Power** | 3S LiPo Battery (11.1V, 2200mAh) | 1 | Power for motors & Pi (via Buck Converter) |
| **IMU** | MPU-6050 ( 6-Axis) | 1 | Accelerometer & Gyroscope data |
| **Distance** | HC-SR04 Ultrasonic Sensor | 1 | Obstacle detection |
| **Chassis** | Aluminum/Acrylic Custom Plate | 1 | Structural Frame |

---

## 🔌 Pinout & Circuitry

### Motor Logic (L298N Connections)
* **L298N Driver 1 (Left Side Motors):**
    * IN1 -> GPIO 17
    * IN2 -> GPIO 27
    * ENA -> GPIO 22 (PWM Speed Control)
* **L298N Driver 2 (Right Side Motors):**
    * IN3 -> GPIO 23
    * IN4 -> GPIO 24
    * ENB -> GPIO 25 (PWM Speed Control)

### Sensor Connections
* **HC-SR04:** Trigger -> GPIO 5 | Echo -> GPIO 6
* **MPU-6050:** SDA -> GPIO 2 (SDA) | SCL -> GPIO 3 (SCL) | VCC -> 3.3V

---

## 💻 Installation & Setup

### 1. Prerequisite Configuration
Ensure your Raspberry Pi is running Raspberry Pi OS and has I2C enabled.
```bash
sudo raspi-config
# Interface Options -> I2C -> Enable
# Interface Options -> GPIO -> Enable
