# Smart Pantry Management System

## Overview
The Smart Pantry Management System is an innovative project that aims to prevent food waste in large storage rooms, such as public food pantries. It utilizes machine learning, camera technology, and an interactive user interface to efficiently manage inventory and reduce food waste.

### Key Features
- Machine learning camera for item detection and expiration date retrieval.
- Object shape detection for optimized storage.
- User-friendly interactive screen for easy management.
- Local database for tracking item locations and expiration dates.

## Table of Contents
- [Getting Started](#getting-started)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Getting Started
Below is all the equipment used to run this project.
1. Raspberry Pi 4 Model B (8GB RAM)
2. 64GB SD Card (64-bit OS installed)
3. Pi Camera
4. Interactive Touch Screen
5. Computer Peripherals
6. Camera Arm Mount
7. Nvidia Jetson Nano (https://www.amazon.com/gp/product/B084DSDDLT/)

## Prerequisites
Install the dependencies below to properly run this project.

```
pip3 install -r requirements.txt
```

```
sudo apt-get update
sudo raspi-config
sudo apt-get install python3-tk
sudo apt-get install python3-opencv
sudo apt-get install tesseract-ocr
sudo apt-get install libtesseract-dev
sudo apt-get install pytesseract
sudo apt-get install libqt4-test
sudo apt-get install -y python3-testresources
```

## Installation
Run the main python file below in the terminal.
```
python3 main.py
```

## Usage
Begin by first running the script, waiting for the GUI to load, then clicking on the Capture button to turn on the camera. It will now show a live feed through the camera and once the item of interest is in position, click anywhere on the screen to capture it and it will show up as a preview on the screen with the date being highlighted and translated. Click one more time to confirm the capture and store the date as a new entry on the table shown in the GUI.

## Resources
- https://docs.ultralytics.com/yolov5/tutorials/pytorch_hub_model_loading/
- https://roboflow.com/convert/yolov8-pytorch-txt-to-yolov5-pytorch-txt
- https://github.com/Qengineering
- https://github.com/Qengineering/TensorFlow_Lite_Segmentation_RPi_32-bit
- https://qengineering.eu/deep-learning-examples-on-raspberry-32-64-os.html
- https://github.com/tutRPi/Raspberry-Pi-OCR-Live-Text-Detection/tree/main
- https://tutorials-raspberrypi.com/raspberry-pi-text-recognition-ocr/
- https://www.tensorflow.org/overview
- https://www.youtube.com/watch?v=yI18t6suGVw
- https://qengineering.eu/install-opencv-on-raspberry-64-os.html
- https://tutorials-raspberrypi.com/raspberry-pi-text-recognition-ocr/
