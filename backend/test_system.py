#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_system.py - Verify semua hardware dan libraries siap
"""

import sys
import os

print("\n" + "="*60)
print("[*] SYSTEM VERIFICATION TEST")
print("="*60 + "\n")

# Test 1: Python environment
print("[1] Python Environment")
print("    Version: " + sys.version.split()[0])
print("    Executable: " + sys.executable)

# Test 2: Required libraries
print("\n[2] Required Libraries")
libs = ['cv2', 'face_recognition', 'flask', 'serial', 'numpy']
missing = []

for lib in libs:
    try:
        __import__(lib)
        print("    OK: " + lib)
    except ImportError:
        print("    MISSING: " + lib)
        missing.append(lib)

if missing:
    print("\n    WARNING: Missing libraries: " + ", ".join(missing))

# Test 3: Camera
print("\n[3] Camera Test")
try:
    import cv2
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if ret:
        print("    OK: Camera available (device 0)")
        print("    Resolution: " + str(frame.shape[1]) + "x" + str(frame.shape[0]))
    else:
        print("    WARNING: Camera device 0 not responding")
except Exception as e:
    print("    ERROR: Camera - " + str(e))

# Test 4: Serial ports
print("\n[4] Serial Ports")
try:
    import serial
    ports = []
    for i in range(20):
        try:
            s = serial.Serial('COM' + str(i), timeout=0.1)
            ports.append('COM' + str(i))
            s.close()
        except:
            pass
    
    if ports:
        print("    OK: Available - " + ", ".join(ports))
    else:
        print("    WARNING: No serial ports found")
except Exception as e:
    print("    ERROR: Serial - " + str(e))

# Test 5: ESP32 connection
print("\n[5] ESP32 Connection")
try:
    import serial
    import time
    
    ser = serial.Serial('COM3', 115200, timeout=2)
    time.sleep(1)
    ser.write(b'status\n')
    time.sleep(0.5)
    resp = ser.read_all()
    ser.close()
    
    if resp:
        print("    OK: ESP32 responding on COM3")
    else:
        print("    WARNING: COM3 open but no response")
except FileNotFoundError:
    print("    ERROR: COM3 not found - Check Device Manager")
except Exception as e:
    print("    WARNING: COM3 - " + str(e))

# Test 6: Dataset
print("\n[6] Face Recognition Dataset")
DATASET_PATH = "../dataset"

try:
    if os.path.exists(DATASET_PATH):
        total_files = 0
        persons = {}
        
        for person in os.listdir(DATASET_PATH):
            folder = os.path.join(DATASET_PATH, person)
            if os.path.isdir(folder):
                files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.png', '.jpeg'))]
                if files:
                    persons[person] = len(files)
                    total_files += len(files)
        
        if persons:
            print("    OK: Dataset found")
            print("    Total files: " + str(total_files))
            print("    Persons: " + ", ".join(sorted(persons.keys())))
        else:
            print("    WARNING: Dataset folder empty")
    else:
        print("    WARNING: Dataset folder not found")
except Exception as e:
    print("    ERROR: Dataset - " + str(e))

# Test 7: Flask template
print("\n[7] Flask Template")
try:
    template_path = "templates/recognition_view_usb.html"
    if os.path.exists(template_path):
        print("    OK: Template found")
    else:
        print("    ERROR: Template not found")
except Exception as e:
    print("    ERROR: Template - " + str(e))

print("\n" + "="*60)
print("VERIFICATION COMPLETE - Ready to run Flask app!")
print("="*60 + "\n")
