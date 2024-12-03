# **Self-Driving Car: Lane Detection and Navigation**

This project implements a Python-based self-driving car system capable of detecting road lines, classifying lane directions, and sending navigation commands to an Arduino via serial communication. The program uses computer vision techniques and integrates with hardware for real-time processing.

---

## **Features**
- **Lane Detection**: Identifies left and right lane markers using Canny edge detection and Hough Line Transform.
- **Direction Classification**: Determines the car's direction relative to the lane (left, right, or centered).
- **Real-Time Communication**: Sends navigation commands (`Left`, `Right`, or `Centered`) to an Arduino controller via serial communication.
- **Interactive Visualization**: Displays lane lines and the classified direction in a live video feed.

---

## **Technologies Used**
- **Programming Language**: Python
- **Libraries**:
  - `cv2` (OpenCV): For image processing and visualization.
  - `numpy`: For numerical calculations.
  - `pyserial`: For serial communication with Arduino.
- **Hardware**:
  - Webcam: For live video feed.
  - Arduino: For motor control.

---

## **Setup and Installation**

### **Prerequisites**
- Install **Python 3.7 or higher**.
- Ensure the following Python libraries are installed:
  ```bash
  pip install opencv-python numpy pyserial

