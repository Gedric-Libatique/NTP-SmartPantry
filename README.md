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
1. Raspberry Pi 4 Model B (8GB RAM) [Link](https://www.amazon.com/Raspberry-Pi-Computer-Suitable-Workstation/dp/B0899VXM8F?th=1)
2. 64GB Micro SD Card [Link](https://www.amazon.com/SanDisk-Ultra-microSDHC-Memory-Adapter/dp/B08GYBBBBH/ref=sr_1_8?c=ts&keywords=Micro%2BSD%2BMemory%2BCards&qid=1704940273&refinements=p_n_feature_two_browse-bin%3A6518305011&s=pc&sr=1-8&ts_id=3015433011&th=1)
3. Tower Cooler for Pi [Link](https://www.amazon.com/dp/B07ZCW27VK?ref_=cm_sw_r_apin_dp_RP8AMZHGYHSWS2KM4JDA&language=en-US)
4. Pi Camera + Lens [Link](https://www.amazon.com/dp/B08LHJR3K4?ref_=cm_sw_r_apin_dp_3A03VH5GXC4WNZKVM9Y7), [Link](https://www.amazon.com/Arducam-Raspberry-CS-Mount-Adjustable-Aperture/dp/B088GWZPL1/ref=pd_bxgy_d_sccl_1/142-2134026-3083828?pd_rd_w=QcjTr&content-id=amzn1.sym.2b132e63-5dcd-4ba1-be9f-9e044543d59f&pf_rd_p=2b132e63-5dcd-4ba1-be9f-9e044543d59f&pf_rd_r=EFJRPH6BD6E58BFGTWBG&pd_rd_wg=QNRpc&pd_rd_r=fcf653e1-cf1c-4068-a609-1fc9c3b48c18&pd_rd_i=B088GWZPL1&psc=1)
5. Pi Camera Extension Cable [Link](https://www.amazon.com/Pastall-Raspberry-15cm%C3%972pcs-30cm%C3%972pcs-50cm%C3%972pcs/dp/B089LM5D1T/ref=sr_1_1_sspa?crid=39S9XN6O7M50F&keywords=ribbon+cable+raspberry+pi+camera&qid=1698701518&sprefix=ribbon+cable+ras%2Caps%2C141&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&psc=1)
6. Interactive Touch Screen [Link](https://www.amazon.com/Lebula-Touchscreen-Raspberry-1024X600-Capacitive/dp/B07VNX4ZWY/ref=sr_1_19?crid=3ICF9D3H2ILBL&keywords=raspberry%2Bpi%2B5%2Btouchscreen%2B7%2Bin&qid=1696818974&sprefix=raspberry%2Bpi%2B5%2Btouchscreen%2B7%2Bin%2Caps%2C130&sr=8-19&th=1)
7. Computer Peripherals [Link](https://www.amazon.com/Waterproof-Compact-Keyboard-Computer-Wireless/dp/B0CJ7XP8LB/ref=sr_1_21?crid=238ZRZQI9SWJ&keywords=small%2Bmouse%2Bkeyboard&qid=1698800392&sprefix=small%2Bmouse%2Bkeyb%2Caps%2C135&sr=8-21&th=1)
8. Camera Arm Mount + Light [Link](https://www.amazon.com/Overhead-Flexible-Articulating-Compatible-Recording/dp/B09ZNNY165/ref=sr_1_10?crid=3QZKXW05ZO94H&keywords=iphone+arm+for+desk&qid=1698714064&sprefix=iphone+arm+for+des%2Caps%2C170&sr=8-10)
9. Wooden Table for Scanning [Link](https://www.amazon.com/Dorel-Home-Products-3536196-Parsons/dp/B01AFUEDBG/ref=sr_1_5?crid=195FJJF1CBX9E&keywords=square%2Bend%2Btable&qid=1698713998&sprefix=square%2Bend%2Btable%2Caps%2C296&sr=8-5&th=1)
10. OPTIONAL: Nvidia Jetson Nano [Link](https://www.amazon.com/gp/product/B084DSDDLT/)

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
