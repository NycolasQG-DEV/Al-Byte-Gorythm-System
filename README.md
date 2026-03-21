<h1 align="center">AI-Byte-Gorythm System | RoboCup 2025</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white" alt="OpenCV" />
  <img src="https://img.shields.io/badge/C++-%2300599C.svg?style=for-the-badge&logo=c%2B%2B&logoColor=white" alt="C++" />
  <img src="https://img.shields.io/badge/Arduino_Mega-00979D?style=for-the-badge&logo=arduino&logoColor=white" alt="Arduino Mega" />
</p>

> **Official repository for the integrated Computer Vision, Artificial Intelligence, and Embedded Control system** of the robot **AI-Byte-Gorythm** (OBR 2024 National Champion and RoboCup 2025 World Highlight).

---

<div align="center">
  <img src="thumb.jpg" alt="AI-Byte-Gorythm Robot Photo" width="600" />
</div>

---

## System Architecture

The robot operates using a **high-performance distributed architecture**, separating intelligence from physical actuation:

* **The Brain (Python + OpenCV):** Runs on the main computer. It processes real-time camera image frames to detect faces, recognize gestures (finger counting via `cvzone`/`MediaPipe`), manage the eye graphics engine on the display, and compute movement logic.
* **The Muscles (C++ + Arduino Mega):** Acts strictly as a *hardware driver*. It receives asynchronous command packets via Serial (e.g., `move_Fwd 150`, `servo 90`), decodes the strings using a custom lightweight parser, and converts instructions into PWM signals for motor controllers (H-Bridge) in a 4WD traction system.

---

## Main Features

* **Automatic Face Tracking:** The robot detects faces on stage and calculates positioning error (X and Y in pixels), converting deviation into automatic rotation and forward/backward adjustments.
* **Hand Gesture Recognition:** Real-time hand landmark mapping. The robot counts the user’s fingers and measures distances to trigger logical commands during the performance.
* **Dynamic Facial Expressions and Audio:** Integrated graphics engine (`pygame`) that reacts to the environment. The eyes blink, change color, display emotions, and synchronize with predefined video/audio files.
* **Custom Serial Parser (C++):** To avoid delays in the hardware main loop, a custom command interpreter was built from scratch on the Arduino. It slices and executes incoming Python packets without relying on heavy libraries.

<br>
---

## How to Run the Project

### 1. Hardware Requirements
* 1 Computer (PC/Notebook/Mini-PC)
* 1 Webcam connected to the PC
* 1 Arduino Mega connected via USB
* 4 DC Motors with H-Bridge drivers and 1 Servo motor

### 2. Setting Up the Muscles (C++)
1. Open the file `AlCode21_05_2025.ino` in the Arduino IDE.
2. Select the **Arduino Mega** board and the correct port.
3. Upload the code. The Arduino will enter listening mode.

### 3. Setting Up the Brain (Python)
Make sure you have Python 3.10+ installed. Install dependencies by running:

    pip install opencv-python cvzone mediapipe pygame pyserial moviepy numpy

### 4. Configuration (`config.py`)
Before running, review the global variables in `config.py`:
* `PORT = "COM20"` → Update to the USB port where your Arduino is connected.
* `DEBUG_MODE = True` → Enable this if you want to run the system in software-only mode (prevents errors when the physical robot is not connected).
* To change the camera → Go to `/functions/camera` and update the `CAMERA` variable (default is 0).

### 5. Start
With everything set up, run from the project root:

    python main.py

---

## Communication Protocol (Serial)

Communication between Python and C++ is handled via space-separated strings. Main commands supported by the Arduino:

| Command        | Parameters              | Description |
|----------------|------------------------|-------------|
| `adjustMotors` | `[m1] [m2] [m3] [m4]`  | Calibrates base power for each of the 4 motors |
| `move_Fwd`     | `[speed] [time]`       | Moves the robot forward using calibrated PWM |
| `servo`        | `[angle]`              | Adjusts camera/head tilt |
| `stop`         | N/A                    | Kill switch. Immediately stops all motors |

---

<div align="center">
  <i>Developed by Nycolas Queiroz Gimenez for the SESI Hortobots robotics team.</i>
</div>
