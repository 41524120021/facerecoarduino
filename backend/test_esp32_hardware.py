#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_esp32_hardware.py - Test ESP32 GPIO outputs (LED, Relay)
"""

import serial
import time

def send_command(command):
    """Send command to ESP32 dan baca response"""
    try:
        ser = serial.Serial('COM3', 115200, timeout=2)
        time.sleep(1)
        
        print(f"\n[*] Sending: {command}")
        ser.write(command.encode() + b'\n')
        
        time.sleep(0.5)
        response = ser.read_all().decode(errors='ignore')
        ser.close()
        
        print(response)
        return True
    except Exception as e:
        print(f"ERROR: {e}")
        return False

print("\n" + "="*60)
print("ESP32 HARDWARE TEST")
print("="*60)

# Test 1: Check status
print("\n[TEST 1] Check ESP32 Status")
send_command("status")

# Test 2: Test LED alone
print("\n[TEST 2] Test LED (blink colors)")
print("Watch LED on GPIO 25/26/27 for rainbow colors...")
send_command("test=LED")
time.sleep(3)

# Test 3: Test Relay alone
print("\n[TEST 3] Test RELAY (pulse)")
print("Listen for relay clicking sound...")
send_command("test=RELAY")
time.sleep(3)

# Test 4: Test door open
print("\n[TEST 4] Test DOOR OPEN (10 seconds)")
print("Watch LED + hear relay + check if door mechanism works...")
send_command("pintu=BUKA")
time.sleep(11)

# Test 5: Manual close
print("\n[TEST 5] Manual DOOR CLOSE")
send_command("pintu=TUTUP")

print("\n" + "="*60)
print("HARDWARE TEST COMPLETE")
print("="*60)
print("\nChecklist:")
print("  [ ] LED berkedip/berubah warna?")
print("  [ ] Relay bunyi (clicking sound)?")
print("  [ ] Pintu mekanisme terangkat/turun?")
print("  [ ] Semua GPIO output bekerja?")
print("\nJika semua OK => Hardware siap!")
print("\n")
