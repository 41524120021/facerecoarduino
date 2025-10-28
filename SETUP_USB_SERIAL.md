# PANDUAN SETUP USB SERIAL DOOR CONTROL
## Face Recognition + ESP32 + USB Serial (Alternatif MQTT)

---

## 📋 DAFTAR ISI
1. [Quick Start (5 Menit)](#quick-start-5-menit)
2. [Hardware Requirements](#hardware-requirements)
3. [Software Setup](#software-setup)
4. [Upload Arduino Sketch](#upload-arduino-sketch)
5. [Jalankan Flask Application](#jalankan-flask-application)
6. [Testing & Troubleshooting](#testing--troubleshooting)
7. [Comparison: MQTT vs USB Serial](#comparison-mqtt-vs-usb-serial)

---

## 🚀 Quick Start (5 Menit)

### Step 1: Siapkan Hardware
- ESP32 DEVKIT V1 dengan USB cable ke PC
- LED (220Ω resistor) ke GPIO 25
- Relay ke GPIO 2
- Webcam USB ke PC

### Step 2: Upload Arduino Sketch
```
File → Open → testbukapintu_serial_usb.ino
Tools → Board: ESP32 Dev Module
Tools → COM Port: COM3 (sesuaikan port Anda)
Upload (Ctrl + U)
```

### Step 3: Install Dependencies Python
```bash
# Di backend folder
pip install pyserial flask opencv-python face-recognition
```

### Step 4: Edit PORT (jika berbeda)
```python
# Buka app_usb.py, ubah:
SERIAL_PORT = "COM3"  # Sesuaikan dengan port Anda
```

### Step 5: Jalankan Aplikasi
```bash
# Di backend folder
python app_usb.py
```

### Step 6: Buka Browser
```
http://localhost:5000
```

**✅ SELESAI! Sistem siap digunakan.**

---

## ⚙️ Hardware Requirements

### Komponen yang Dibutuhkan:
- **1x ESP32 DEVKIT V1** (main microcontroller)
- **1x LED Red** + **1x Resistor 220Ω** (indikator)
- **1x Relay Module** 5V (kontrol pintu)
- **1x USB Cable** Type-B (koneksi ke PC)
- **1x Power Supply** 5V 2A (untuk relay - PENTING!)
- **1x Webcam USB** (face recognition)

### Wiring Diagram:
```
ESP32 PIN 25 → [220Ω Resistor] → LED Anode
ESP32 GND   → LED Katode

ESP32 PIN 2  → Relay Signal Pin
Relay GND   → ESP32 GND
Relay 5V    → External Power Supply 5V
Relay NO/C  → Solenoid/Maglock 12V

PC USB      → ESP32 USB (for serial communication)
PC USB      → Webcam USB
```

**⚠️ PENTING:** Relay HARUS menggunakan external power supply 5V, bukan dari ESP32!
ESP32 hanya memberikan sinyal kontrol (3.3V logic).

---

## 💻 Software Setup

### 1. Install Arduino IDE & ESP32 Board
```
Arduino IDE → Preferences → 
Board Manager URL: https://dl.espressif.com/dl/package_esp32_index.json
→ Install esp32 by Espressif Systems
```

### 2. Install Python Dependencies
```bash
# Buka terminal di folder backend
pip install pyserial flask opencv-python face-recognition numpy

# Atau gunakan requirements.txt jika ada:
# pip install -r requirements.txt
```

### 3. Verifikasi Port COM
```powershell
# Windows PowerShell - Cari COM port ESP32
Get-WmiObject Win32_SerialPort | Select-Object Name, Description

# Output contoh:
# Name         Description
# ----         -----------
# COM3         USB-SERIAL CH340 (COM3)
```

Catat port-nya (biasanya COM3 atau COM4)

### 4. Edit Konfigurasi Flask
```python
# app_usb.py, ubah sesuai port Anda:
SERIAL_PORT = "COM3"        # Ganti COM3 dengan port Anda
SERIAL_BAUDRATE = 115200    # Jangan diubah!
DATASET_PATH = "../dataset" # Folder dataset wajah
```

---

## 📤 Upload Arduino Sketch

### Step-by-Step:

1. **Buka Arduino IDE**
   ```
   File → Open → testbukapintu_serial_usb.ino
   ```

2. **Pilih Board & Port**
   ```
   Tools → Board → ESP32 Dev Module
   Tools → Port → COM3 (sesuaikan dengan port Anda)
   ```

3. **Verify Sketch** (optional, untuk cek error)
   ```
   Sketch → Verify/Compile (Ctrl + R)
   ```

4. **Upload ke Board**
   ```
   Sketch → Upload (Ctrl + U)
   atau klik tombol Upload (panah kanan)
   ```

5. **Monitor Output** (untuk debug)
   ```
   Tools → Serial Monitor (Ctrl + Shift + M)
   Set baud rate: 115200
   
   Output contoh:
   [ESP32] Serial initialized at 115200 baud
   [ESP32] Waiting for commands...
   ```

### Jika Terjadi Error:

**Error: "Board not found"**
- Pastikan driver CH340 sudah install: https://ch340.com
- Restart Arduino IDE
- Coba port COM lain

**Error: "Permission denied"**
- Close Serial Monitor dulu sebelum upload
- Tunggu 2-3 detik
- Upload lagi

**Error: "Upload timeout"**
- Cabut USB cable → Tunggu 3 detik → Colok kembali
- Coba upload lagi

---

## 🐍 Jalankan Flask Application

### Setup Virtual Environment (Recommended):
```bash
# Buka terminal di folder backend
python -m venv venv

# Activate venv:
# Windows PowerShell:
.\venv\Scripts\Activate.ps1

# Jika error permission denied:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Install Dependencies:
```bash
pip install pyserial flask opencv-python face-recognition numpy
```

### Edit Dataset Path (jika perlu):
```python
# app_usb.py
DATASET_PATH = "../dataset"  # Pastikan folder ini ada!
```

### Jalankan Aplikasi:
```bash
python app_usb.py
```

**Expected Output:**
```
 ╔═══════════════════════════════════════════════════╗
 ║   Face Recognition + USB Serial Door Control    ║
 ╚═══════════════════════════════════════════════════╝

✅ Serial COM3 terhubung!
✅ Siap digunakan!

 * Serving Flask app 'Flask'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Buka Browser:
```
http://localhost:5000
```

---

## 🧪 Testing & Troubleshooting

### Test 1: Cek Koneksi Serial
```python
# Buka Python interpreter
from esp32_serial import ESP32SerialController

esp32 = ESP32SerialController("COM3", 115200)
if esp32.open():
    print("✅ Koneksi OK")
    esp32.close()
else:
    print("❌ Koneksi gagal")
```

### Test 2: Test LED
```python
esp32 = ESP32SerialController("COM3", 115200)
esp32.open()
esp32.test_led()  # LED akan berkedip
esp32.close()
```

### Test 3: Test Relay
```python
esp32 = ESP32SerialController("COM3", 115200)
esp32.open()
esp32.test_relay()  # Relay akan aktif 1 detik
esp32.close()
```

### Test 4: Test Door Control
```python
esp32 = ESP32SerialController("COM3", 115200)
esp32.open()
esp32.buka_pintu()  # Pintu buka 10 detik
esp32.close()
```

### Test 5: Check Status di Web Interface
```
1. Buka http://localhost:5000
2. Lihat indicator ESP32 Status di atas
3. Seharusnya berwarna hijau "✅ Terhubung"
4. Klik tombol "Test LED" → LED ESP32 akan berkedip
5. Klik tombol "Test Relay" → Relay akan aktif
```

---

## 🔍 Troubleshooting

### Problem: "Serial port COM3 tidak ditemukan"
```
Solusi:
1. Cek Device Manager → Ports (COM & LPT)
2. Pastikan ESP32 muncul di sana
3. Jika tidak, install driver CH340: https://ch340.com
4. Ubah SERIAL_PORT di app_usb.py ke port yang benar
```

### Problem: "Permission denied" saat connect serial
```
Solusi:
1. Close Serial Monitor di Arduino IDE
2. Jalankan Flask app lagi
3. Jika masih error, restart PC
```

### Problem: "LED tidak menyala / Relay tidak berbunyi"
```
Solusi:
1. Cek wiring:
   - LED → GPIO 25 + resistor 220Ω → GND
   - Relay → GPIO 2 → GND
2. Cek relay external power (5V) terhubung
3. Buka Serial Monitor Arduino IDE → cek output:
   [ESP32] Perintah diterima: pintu=BUKA
4. Jika ada error, berarti sketch tidak upload dengan benar
```

### Problem: "Face tidak terdeteksi"
```
Solusi:
1. Cek webcam sudah connect
2. Cek Dataset folder ada: ../dataset/
3. Cek ada foto wajah di: ../dataset/nama_orang/
4. Cek Python berhasil load dataset:
   - Buka Python interpreter
   - import face_recognition
   - Check dataset dapat di-load
5. Jika tidak, tambah foto training ke dataset folder
```

### Problem: "Web page tidak bisa diakses"
```
Solusi:
1. Cek Flask app running (lihat console)
2. Akses http://127.0.0.1:5000 (bukan localhost)
3. Cek firewall tidak block port 5000
4. Cek port 5000 tidak digunakan aplikasi lain:
   netstat -an | find ":5000"
```

### Problem: "ESP32 terputus setiap beberapa menit"
```
Solusi:
1. Ganti USB cable (cable berkualitas penting)
2. Gunakan USB port di belakang PC/hub (bukan USB extension)
3. Tambah external power untuk ESP32 (5V 2A)
4. Cek app.py, pastikan serial connection di-maintain
```

---

## 📊 Comparison: MQTT vs USB Serial

| Aspek | MQTT | USB Serial |
|-------|------|-----------|
| **Kecepatan Respons** | 1-2 detik | < 100ms (INSTANT) |
| **Jarak Komunikasi** | Unlimited (internet) | Max 5 meter (USB cable) |
| **Internet Required** | ✅ Ya | ❌ Tidak |
| **Kompleksitas Setup** | Medium | Simple |
| **Scalability** | Bisa banyak device | 1 device per COM port |
| **Performa Broker** | Tergantung broker | N/A |
| **Use Case** | Remote/cloud control | Local fast control |

### Kapan Gunakan USB Serial:
- ✅ Pintu ada di kantor (local)
- ✅ Perlu respons cepat (< 100ms)
- ✅ Tidak perlu remote access
- ✅ WiFi tidak stabil
- ✅ Biaya internet mahal

### Kapan Gunakan MQTT:
- ✅ Pintu di lokasi berbeda
- ✅ Perlu remote access
- ✅ Multiple door/device
- ✅ Internet connection available

---

## 📝 Command Reference

### Arduino Serial Commands:

| Command | Efek | Response |
|---------|------|----------|
| `pintu=BUKA` | LED ON, Relay ON (10s) | `Pintu dibuka 10 detik` |
| `pintu=TUTUP` | LED OFF, Relay OFF | `Pintu ditutup` |
| `test=LED` | LED blink 3x | `LED test done` |
| `test=RELAY` | Relay ON 1s | `RELAY test done` |
| `status` | Get status | `LED: [ON/OFF], RELAY: [ON/OFF]` |

### Python Serial Library:

```python
from esp32_serial import ESP32SerialController

# Inisialisasi
esp32 = ESP32SerialController("COM3", 115200)
esp32.open()

# Kontrol Pintu
esp32.buka_pintu()      # Buka 10 detik
esp32.tutup_pintu()     # Tutup immediate

# Test
esp32.test_led()        # Test LED
esp32.test_relay()      # Test Relay

# Status
esp32.get_status()      # Get status

# Close connection
esp32.close()
```

---

## 🔐 Security Notes

1. **Jangan publish port serial ke internet**
   - USB Serial hanya untuk local use
   - Jika perlu remote, gunakan MQTT dengan password

2. **Pastikan dataset wajah aman**
   - Limit access ke folder dataset/
   - Jangan share dataset folder ke public

3. **Monitor door access**
   - Log semua pembukaan pintu
   - Check aplikasi presensi.php untuk history

4. **Test button accuracy**
   - Pastikan face recognition accuracy tinggi
   - Test dengan cahaya berbeda
   - Tambah foto training jika perlu

---

## 📞 Quick Fixes

**Sesuatu error?** Coba:
1. Restart aplikasi Flask
2. Unplug USB cable → tunggu 3s → plug kembali
3. Buka Serial Monitor untuk debug
4. Check internet connection (jika ada network issue)
5. Reinstall pyserial: `pip install --upgrade pyserial`

---

## 🎯 Next Steps

1. ✅ Upload Arduino sketch
2. ✅ Install Python dependencies
3. ✅ Run Flask application
4. ✅ Test web interface
5. ⏳ Train face recognition (add photos to dataset/)
6. ⏳ Configure dashboard (PHP)
7. ⏳ Deploy ke production

---

**Selesai! Sistem sudah siap digunakan dengan USB Serial yang cepat dan reliable.** 🚀

Jika ada pertanyaan, cek troubleshooting section atau Arduino Serial Monitor untuk debug.

