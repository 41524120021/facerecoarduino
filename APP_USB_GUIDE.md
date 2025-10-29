# 🎯 APP_USB & APP_USB_MINIMAL - Flask Web Interface dengan Door Control

Dua aplikasi Flask untuk mengontrol ESP32 pintu via USB Serial dengan atau tanpa face recognition.

---

## 📊 PERBANDINGAN

| Feature | test_esp32_web.py | app_usb_minimal.py | app_usb.py |
|---------|------------------|--------------------|------------|
| **Startup Time** | ⚡ Instant | ⚡ Instant | 🐢 ~30+ detik |
| **Face Recognition** | ❌ No | ❌ No | ✅ Yes |
| **Dataset Loading** | N/A | N/A | ✅ Load at startup |
| **Port** | 5000 | 5001 | 5000 (sebelum fix) |
| **Use Case** | Pure ESP32 testing | Quick demo + door control | Full production |
| **Dependencies** | Flask, pyserial | Flask, opencv, pyserial | Flask, opencv, face-recognition |

---

## 🚀 QUICK START

### 1️⃣ **test_esp32_web.py** (Pure ESP32 Testing)

**Best for:** Testing LED, Relay, dan Door control tanpa perlu camera atau face recognition.

```bash
cd backend
python test_esp32_web.py
# http://127.0.0.1:5000
```

**Fitur:**
- ✅ Real-time status indicator
- ✅ LED test
- ✅ Relay test
- ✅ Door control (10s)
- ✅ Auto-refresh status

---

### 2️⃣ **app_usb_minimal.py** (Fast Loading with UI)

**Best for:** Demo, presentation, atau cepat test tanpa face recognition overhead.

```bash
cd backend
python app_usb_minimal.py
# http://127.0.0.1:5001
```

**Fitur:**
- ✅ Video stream dari camera (MJPEG)
- ✅ Door control buttons
- ✅ Fast startup (~2 detik)
- ✅ No face recognition (skip dataset loading)
- ✅ Minimal dependencies

**Tampilan:**
```
┌─────────────────────────────────────┐
│  LIVE FEED                          │
│  [Camera Stream MJPEG]              │
├─────────────────────────────────────┤
│  Last: - | 2025-10-28 16:00:00      │
├─────────────────────────────────────┤
│  [🔓 BUKA PINTU]  [🔒 TUTUP PINTU]  │
│  [💡 TEST LED]    [⚡ TEST RELAY]   │
└─────────────────────────────────────┘
```

---

### 3️⃣ **app_usb.py** (Full Production Version)

**Best for:** Production environment dengan face recognition enabled.

```bash
cd backend
python app_usb.py
# http://127.0.0.1:5000 (note: different port after fix)
```

**Fitur:**
- ✅ Video stream dengan face detection
- ✅ Wajah recognition (dataset loading)
- ✅ Presensi logging
- ✅ Door control
- ❌ Slow startup (dataset loading)

**Improvements Made:**
```python
# Before: debug=True (causes PermissionError on COM3 restart)
app.run(debug=True, host='127.0.0.1', port=5000)

# After: debug=False (stable connection)
app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)
```

---

## 🔧 INSTALASI DEPENDENCIES

### Untuk test_esp32_web.py (Minimal)
```bash
pip install flask pyserial
```

### Untuk app_usb_minimal.py
```bash
pip install flask pyserial opencv-python
```

### Untuk app_usb.py (Full)
```bash
pip install flask pyserial opencv-python face-recognition
# atau
pip install -r requirements.txt
```

**Note:** face-recognition requires dlib, yang memerlukan compiler. Gunakan `dlib-bin` untuk pre-compiled version:
```bash
pip install dlib-bin
```

---

## 🎮 USING test_esp32_web.py

### Tombol Kontrol:

| Button | Action |
|--------|--------|
| **🔓 Buka Pintu** | Open door for 10 seconds + LED blinking + relay pulsing |
| **🔒 Tutup Pintu** | Close door immediately |
| **💡 Test LED** | Test LED (blink/color) |
| **⚡ Test Relay** | Test Relay (pulse sound) |
| **🔄 Refresh** | Manual status refresh |

### Status Indicator:

```
🟢 ✅ Terhubung     → ESP32 ready, buttons enabled
🔴 ❌ Terputus      → ESP32 not connected, buttons disabled
```

---

## 🎮 USING app_usb_minimal.py

### Layout:

1. **Video Feed** (Live camera stream)
   - MJPEG format (motion JPEG)
   - Real-time display

2. **Status** (Last detected person)
   - Shows: "Last: [nama] | [waktu]"

3. **Controls** (Door + Test buttons)
   - Buka Pintu / Tutup Pintu
   - Test LED / Test Relay

### Differences from test_esp32_web:
- Includes video feed (camera required)
- More UI elements for presentation
- Same port (5001)
- No face recognition processing (instant response)

---

## 🎮 USING app_usb.py

### Features:

1. **Video Feed with Face Detection**
   - Real-time face detection
   - Known faces highlighted in GREEN
   - Unknown faces highlighted in RED

2. **Auto Presensi Logging**
   - When face detected → POST to `presensi.php`
   - 5-second debounce (prevent duplicate logging)
   - Automatic timestamp

3. **Door Control**
   - Manual button click
   - Triggered on face recognition (future: auto-open for known faces)

### Status Display:
```
Last Detected: [Nama Orang] | [Timestamp]
- Updates every frame if new face detected
- Resets to "-" after 5 seconds without detection
```

---

## 🔌 SERIAL COMMUNICATION

### Commands (ESP32):

```
Command         | Response
----------------|------------------------------------------
pintu=BUKA      | Door opens, LED blinks, Relay pulses (10s)
pintu=TUTUP     | Door closes, LED OFF, Relay OFF
test=LED        | LED test (blink or color change)
test=RELAY      | Relay pulse (2 seconds)
status          | Return current status
```

### Port Configuration:

Edit dalam setiap file:
```python
SERIAL_PORT = "COM3"           # Windows
# atau
SERIAL_PORT = "/dev/ttyUSB0"   # Linux
SERIAL_BAUDRATE = 115200        # Fixed
```

---

## ⚡ TROUBLESHOOTING

### Problem 1: "PermissionError: could not open port 'COM3'"

**Causes:**
- Arduino IDE Serial Monitor masih terbuka
- Aplikasi lain menggunakan COM3
- Driver CH340 tidak installed

**Solutions:**
1. Close Arduino IDE + Serial Monitor
2. Close aplikasi lain yang pakai serial
3. Install CH340 driver dari Silicon Labs
4. Restart PC jika perlu

### Problem 2: Flask tidak bisa start

**Cause:** Port sudah dipakai aplikasi lain

**Solution:**
```bash
# Kill existing Python processes
taskkill /f /im python.exe

# Atau ubah port di code:
app.run(..., port=5005)  # Use different port
```

### Problem 3: Dataset loading terlalu lama

**Symptoms:**
- App startup > 1 minute
- App frozen while loading faces
- KeyboardInterrupt saat loading

**Solutions:**
1. Use `app_usb_minimal.py` instead (skip face recognition)
2. Reduce dataset size (fewer person folders)
3. Use lower resolution images
4. Atau tunggu lebih lama (~2-3 menit untuk 1000+ images)

### Problem 4: Camera tidak terdeteksi

**Symptoms:**
- Black/empty video feed
- cv2.VideoCapture(0) fails

**Solutions:**
```python
# Test dengan device index lain:
camera = cv2.VideoCapture(0)   # Try 0, 1, 2, -1
camera = cv2.VideoCapture(1)   # Jika 0 tidak bekerja
```

### Problem 5: Face recognition accuracy rendah

**Causes:**
- Bad lighting
- Face angle > 45 degrees
- Low resolution images
- Small face in frame

**Solutions:**
1. Better lighting
2. Face straight to camera
3. Increase image resolution
4. Move closer to camera

---

## 📱 REMOTE ACCESS

Default: `localhost` (127.0.0.1) only

Untuk akses dari network lain:
```python
# Change in app.run():
app.run(debug=False, host='0.0.0.0', port=5001)
# Then access: http://[PC_IP]:5001
```

**Warning:** Jangan expose ke internet tanpa security!

---

## 🚀 DEPLOYMENT

### Development:
```bash
python app_usb_minimal.py    # atau test_esp32_web.py
```

### Production:
```bash
# Use Gunicorn instead of built-in Flask server:
pip install gunicorn
gunicorn -w 1 -b 127.0.0.1:5001 app_usb_minimal:app

# Atau Waitress (Windows):
pip install waitress
waitress-serve --port=5001 app_usb_minimal:app
```

---

## 📊 QUICK COMPARISON TABLE

```
┌──────────────────┬────────────┬──────────────┬─────────────┐
│ Aplikasi         │ Startup    │ Dependencies │ Use Case    │
├──────────────────┼────────────┼──────────────┼─────────────┤
│ test_esp32_web   │ Instant    │ Minimal      │ ESP32 test  │
│ app_usb_minimal  │ 2-3 detik  │ +OpenCV      │ Quick demo  │
│ app_usb.py       │ 30+ detik  │ +face_recog  │ Production  │
└──────────────────┴────────────┴──────────────┴─────────────┘
```

---

## 🎯 RECOMMENDED WORKFLOW

1. **Testing Phase:**
   ```bash
   # Verify hardware works
   python test_esp32_web.py
   # Test: LED, Relay, Door control
   ```

2. **Demo Phase:**
   ```bash
   # Show UI with camera
   python app_usb_minimal.py
   # Demonstrate real interface
   ```

3. **Production Phase:**
   ```bash
   # Full face recognition enabled
   python app_usb.py
   # Monitor presensi logs
   # Auto door unlock on face match
   ```

---

## 🔗 RELATED FILES

- `esp32_serial.py` - Serial communication library
- `requirements.txt` - Dependency list
- `arduino/testbukapintu_serial_usb*/` - Arduino sketches
- `TEST_ESP32_WEB_GUIDE.md` - Detailed test guide
- `backend/templates/recognition_view_usb.html` - UI template

---

## 📞 SUPPORT

Check logs for debugging:
```bash
# Run with verbose output
python -u app_usb.py  # Force unbuffered output
```

Common error messages:
- `ModuleNotFoundError` → pip install missing package
- `PermissionError` → Close Serial Monitor or conflicting app
- `FileNotFoundError` → Check DATASET_PATH or template paths

---

**Status:** ✅ Ready for testing and production use!

