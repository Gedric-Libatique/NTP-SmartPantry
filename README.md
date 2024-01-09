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
Listed below is all the equipment used to run this project.
1. Raspberry Pi 4 Model B (8GB RAM)
2. 64GB SD Card (64-bit OS installed)
3. Pi Camera
4. Interactive Touch Screen
5. Computer Peripherals
6. Camera Arm Mount

## Prerequisites
The prerequisites below are needed to run this project.
- https://qengineering.eu/install-opencv-on-raspberry-64-os.html
- Install dependencies:

```
sudo apt install tesseract-ocr
```

```
pip3 install -r requirements.txt
```

## Installation
Detect text in images or a camera live feed
Tutorial: https://tutorials-raspberrypi.com/raspberry-pi-text-recognition-ocr/

1. Run Examples

```
python3 example.py
python3 live.py
```

## Usage
Explain how to use your Smart Pantry Management System. Include examples, screenshots, or code snippets if necessary.

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
