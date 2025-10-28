#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_esp32_serial.py - ESP32 USB Serial Testing Tool
Gunakan script ini untuk test connection dan kontrol ESP32 via USB Serial
"""

import sys
import time
from pathlib import Path

# Coba import library custom (jika ada)
try:
    from esp32_serial import ESP32SerialController
except ImportError:
    print("⚠️  esp32_serial tidak ditemukan!")
    print("   Pastikan esp32_serial.py ada di folder ini")
    sys.exit(1)

# ============================================================
# WARNA OUTPUT
# ============================================================
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    END = '\033[0m'

def print_success(msg):
    print(f"{Colors.GREEN}✅ {msg}{Colors.END}")

def print_error(msg):
    print(f"{Colors.RED}❌ {msg}{Colors.END}")

def print_warning(msg):
    print(f"{Colors.YELLOW}⚠️  {msg}{Colors.END}")

def print_info(msg):
    print(f"{Colors.CYAN}ℹ️  {msg}{Colors.END}")

def print_header(msg):
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}{msg:^50}{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}\n")

# ============================================================
# TEST FUNCTIONS
# ============================================================

def test_connection(port, baudrate):
    """Test koneksi ke ESP32"""
    print_header("TEST 1: Koneksi Serial")
    
    try:
        esp32 = ESP32SerialController(port, baudrate)
        if esp32.open():
            print_success(f"Berhasil connect ke {port} @ {baudrate} bps")
            esp32.close()
            return True
        else:
            print_error(f"Gagal membuka serial port {port}")
            return False
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_led(port, baudrate):
    """Test LED"""
    print_header("TEST 2: LED Control (GPIO 25)")
    
    try:
        esp32 = ESP32SerialController(port, baudrate)
        if not esp32.open():
            print_error("Tidak dapat connect ke ESP32")
            return False
        
        print_info("Mengirim perintah: test=LED")
        esp32.send_command("test=LED")
        time.sleep(1)
        
        responses = esp32.read_response(5)
        if responses:
            print_success(f"LED test dikirim")
            for r in responses:
                print(f"  ← {r}")
        else:
            print_warning("Tidak ada response dari ESP32")
        
        esp32.close()
        return True
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_relay(port, baudrate):
    """Test Relay"""
    print_header("TEST 3: Relay Control (GPIO 2)")
    
    try:
        esp32 = ESP32SerialController(port, baudrate)
        if not esp32.open():
            print_error("Tidak dapat connect ke ESP32")
            return False
        
        print_info("Mengirim perintah: test=RELAY")
        esp32.send_command("test=RELAY")
        time.sleep(1)
        
        responses = esp32.read_response(5)
        if responses:
            print_success(f"RELAY test dikirim")
            for r in responses:
                print(f"  ← {r}")
        else:
            print_warning("Tidak ada response dari ESP32")
        
        esp32.close()
        return True
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_door_control(port, baudrate):
    """Test Kontrol Pintu"""
    print_header("TEST 4: Door Control (pintu=BUKA)")
    
    try:
        esp32 = ESP32SerialController(port, baudrate)
        if not esp32.open():
            print_error("Tidak dapat connect ke ESP32")
            return False
        
        print_info("Mengirim perintah: pintu=BUKA")
        print_info("Pintu akan terbuka selama 10 detik...")
        
        esp32.send_command("pintu=BUKA")
        
        # Monitor selama 10 detik
        start_time = time.time()
        while time.time() - start_time < 10:
            responses = esp32.read_response(3)
            if responses:
                for r in responses:
                    print(f"  ← {r}")
            time.sleep(0.5)
        
        print_success("Pintu auto-closed (10 detik selesai)")
        esp32.close()
        return True
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def test_status(port, baudrate):
    """Test Get Status"""
    print_header("TEST 5: Get Status")
    
    try:
        esp32 = ESP32SerialController(port, baudrate)
        if not esp32.open():
            print_error("Tidak dapat connect ke ESP32")
            return False
        
        print_info("Mengirim perintah: status")
        esp32.send_command("status")
        time.sleep(0.5)
        
        responses = esp32.read_response(5)
        if responses:
            print_success("Status diterima:")
            for r in responses:
                print(f"  {r}")
        else:
            print_warning("Tidak ada response")
        
        esp32.close()
        return True
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def interactive_mode(port, baudrate):
    """Mode interaktif - kirim command custom"""
    print_header("INTERACTIVE MODE")
    
    try:
        esp32 = ESP32SerialController(port, baudrate)
        if not esp32.open():
            print_error("Tidak dapat connect ke ESP32")
            return False
        
        print("Ketik command (atau 'exit' untuk keluar):")
        print("Commands: pintu=BUKA, pintu=TUTUP, test=LED, test=RELAY, status")
        print()
        
        while True:
            try:
                cmd = input(">>> ").strip()
                
                if cmd.lower() == 'exit':
                    break
                if not cmd:
                    continue
                
                print(f"Sending: {cmd}")
                esp32.send_command(cmd)
                time.sleep(0.5)
                
                responses = esp32.read_response(10)
                if responses:
                    for r in responses:
                        print(f"  ← {r}")
                else:
                    print_warning("No response")
                    
            except KeyboardInterrupt:
                print("\nAborted.")
                break
            except Exception as e:
                print_error(f"Error: {e}")
        
        esp32.close()
        return True
    except Exception as e:
        print_error(f"Exception: {e}")
        return False

def show_menu():
    """Tampilkan menu pilihan"""
    print()
    print("Pilih test yang akan dijalankan:")
    print("  1. Test Connection (basic)")
    print("  2. Test LED (GPIO 25)")
    print("  3. Test Relay (GPIO 2)")
    print("  4. Test Door Control (FULL)")
    print("  5. Get Status")
    print("  6. Interactive Mode (custom commands)")
    print("  7. Run All Tests")
    print("  0. Exit")
    print()

# ============================================================
# MAIN
# ============================================================

def main():
    print_header("ESP32 USB SERIAL TESTING TOOL")
    
    # Default port
    port = "COM3"
    baudrate = 115200
    
    # Tanya port jika berbeda
    print("╔═══════════════════════════════════════╗")
    print("║  Konfigurasi Serial Connection      ║")
    print("╚═══════════════════════════════════════╝")
    print()
    
    user_port = input(f"Port (default={port}): ").strip()
    if user_port:
        port = user_port
    
    print_info(f"Using port: {port} @ {baudrate} bps")
    print()
    
    while True:
        show_menu()
        choice = input("Pilihan (1-7, 0=exit): ").strip()
        
        if choice == '0':
            print_info("Goodbye!")
            break
        elif choice == '1':
            test_connection(port, baudrate)
        elif choice == '2':
            test_led(port, baudrate)
        elif choice == '3':
            test_relay(port, baudrate)
        elif choice == '4':
            test_door_control(port, baudrate)
        elif choice == '5':
            test_status(port, baudrate)
        elif choice == '6':
            interactive_mode(port, baudrate)
        elif choice == '7':
            # Run all tests
            results = []
            results.append(("Connection", test_connection(port, baudrate)))
            results.append(("LED", test_led(port, baudrate)))
            results.append(("Relay", test_relay(port, baudrate)))
            results.append(("Status", test_status(port, baudrate)))
            
            print_header("TEST SUMMARY")
            for name, result in results:
                status = "✅ PASS" if result else "❌ FAIL"
                print(f"{name:20} → {status}")
        else:
            print_warning("Invalid choice")
        
        input("\n[Press ENTER to continue...]")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Interrupted by user{Colors.END}")
        sys.exit(0)
    except Exception as e:
        print_error(f"Fatal error: {e}")
        sys.exit(1)
