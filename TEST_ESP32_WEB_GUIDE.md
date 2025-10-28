# 🚀 TEST_ESP32_WEB.PY - Flask Web Interface untuk ESP32 Testing

Aplikasi Flask sederhana untuk test LED, Relay, dan Door Control via USB Serial.

---

## ✨ FITUR

✅ **Web Interface** - Simple dan user-friendly  
✅ **Status Indicator** - Real-time ESP32 connection status  
✅ **Door Control** - Buka pintu 10 detik / Tutup immediate  
✅ **LED Test** - Test LED berkedip/berwarna  
✅ **Relay Test** - Test relay bunyi/pulsing  
✅ **Auto Refresh** - Status check setiap 2 detik  
✅ **Responsive Design** - Mobile-friendly UI  

---

## 🚀 QUICK START

### 1. Install Dependencies (HANYA SEKALI)
```bash
cd backend
pip install flask pyserial
```

### 2. Upload Arduino Sketch ke ESP32
```
Arduino IDE → File → Open → 
  arduino/testbukapintu_serial_usb/testbukapintu_serial_usb.ino
→ Tools → Board: ESP32 Dev Module
→ Tools → Port: COM3 (sesuaikan port Anda)
→ Upload (Ctrl+U)
```

### 3. Jalankan Flask Server
```bash
cd backend
python test_esp32_web.py
```

**Output:**
```
╔═══════════════════════════════════════════════════╗
║   ESP32 USB Serial Test Web Interface           ║
╚═══════════════════════════════════════════════════╝

✅ Serial COM3 terhubung!
✅ Siap digunakan!

🚀 Starting Flask server...
📍 Open: http://127.0.0.1:5000
```

### 4. Buka Browser
```
http://127.0.0.1:5000
```

**Selesai!** Web interface siap digunakan. 🎉

---

## 🎮 CARA MENGGUNAKAN

### Status Indicator
```
🟢 Hijau (✅ Terhubung)     → ESP32 ready, tombol aktif
🔴 Merah (❌ Terputus)      → ESP32 tidak terhubung, tombol disable
```

### Tombol Kontrol

**🔓 Buka Pintu (10s)**
- Membuka pintu selama 10 detik
- LED akan berkedip/berubah warna
- Relay akan bunyi pulsing
- Auto-tutup setelah 10 detik

**🔒 Tutup Pintu**
- Menutup pintu immediate
- LED OFF, Relay OFF

**💡 Test LED**
- LED berkedip 3x (original version)
- Atau tampilkan semua warna (RGB version)

**⚡ Test Relay**
- Relay bunyi pulsing selama 2 detik

**🔄 Refresh Status**
- Manual refresh status koneksi

---

## 📝 KONFIGURASI

Edit `test_esp32_web.py` untuk mengubah:

```python
# Line 15-16
SERIAL_PORT = "COM3"           # Ubah sesuai port Anda
SERIAL_BAUDRATE = 115200       # Jangan diubah!
```

Contoh perubahan port:
```python
SERIAL_PORT = "COM4"           # Jika port Anda COM4
SERIAL_PORT = "/dev/ttyUSB0"   # Linux/Mac
```

---

## 🔧 TROUBLESHOOTING

### Problem 1: "ESP32 tidak terhubung"
```
Solusi:
1. Cek ESP32 sudah connect via USB (lihat Device Manager)
2. Cek driver CH340 sudah installed
3. Ubah SERIAL_PORT ke port yang benar
4. Restart aplikasi Flask
```

### Problem 2: "Permission denied" error
```
Solusi:
1. Close Serial Monitor di Arduino IDE (konflik port)
2. Restart aplikasi Flask
3. Atau restart PC
```

### Problem 3: "ModuleNotFoundError: No module named 'serial'"
```
Solusi:
pip install pyserial
```

### Problem 4: Tombol tidak aktif (disable)
```
Solusi:
1. Status indicator harus hijau (✅ Terhubung)
2. Cek ESP32 USB connection
3. Klik "🔄 Refresh Status" untuk manual refresh
```

### Problem 5: Tidak ada response dari ESP32
```
Solusi:
1. Check Arduino Serial Monitor apakah sketch sudah upload
2. Ubah COM port di test_esp32_web.py
3. Buka Serial Monitor untuk verify sketch berjalan:
   Tools → Serial Monitor (Ctrl+Shift+M)
   Baud: 115200
   [Lihat startup message dari ESP32]
```

---

## 🧪 TESTING WORKFLOW

```
1. Run aplikasi Flask
   python test_esp32_web.py

2. Buka browser http://127.0.0.1:5000

3. Tunggu status indicator hijau ✅ Terhubung

4. Test tombol satu per satu:
   a. 💡 Test LED
   b. ⚡ Test Relay
   c. 🔓 Buka Pintu (lihat LED + dengarkan relay)
   d. 🔒 Tutup Pintu

5. Verifikasi fisik:
   - LED harus berkedip/berubah warna
   - Relay harus berbunyi pulsing
   - Pintu harus buka selama 10 detik
```

---

## 📊 RESPONSE EXAMPLES

### Success Response (Buka Pintu)
```json
{
  "status": "OK",
  "message": "Pintu dibuka selama 10 detik",
  "response": [
    "🔓 BUKA PINTU!",
    "💡 LED berkedip + 📣 RELAY pulsing (10 detik)",
    "⏱️  Tunggu 10 detik...",
    ".🔊.🔊... (10 detik)"
  ]
}
```

### Error Response (Not Connected)
```json
{
  "status": "ERROR",
  "message": "ESP32 tidak terhubung"
}
```

---

## 🔗 API ENDPOINTS

```
GET  /                         Main page (HTML)
GET  /api/serial_status        Check ESP32 connection status
POST /api/buka_pintu           Open door (10s)
POST /api/tutup_pintu          Close door
POST /api/test_led             Test LED
POST /api/test_relay           Test Relay
```

### Curl Examples

```bash
# Check status
curl http://127.0.0.1:5000/api/serial_status

# Buka pintu
curl -X POST http://127.0.0.1:5000/api/buka_pintu

# Tutup pintu
curl -X POST http://127.0.0.1:5000/api/tutup_pintu

# Test LED
curl -X POST http://127.0.0.1:5000/api/test_led

# Test Relay
curl -X POST http://127.0.0.1:5000/api/test_relay
```

---

## 🎨 UI FEATURES

### Responsive Design
- ✅ Desktop (800px+)
- ✅ Tablet (600px+)
- ✅ Mobile (320px+)

### Visual Feedback
- ✅ Status indicator (connected/disconnected)
- ✅ Alert messages (success/error)
- ✅ Button hover effects
- ✅ Button loading state

### Real-time Status
- ✅ Auto-refresh setiap 2 detik
- ✅ Manual refresh button
- ✅ Connection loss detection

---

## 📚 FULL WORKFLOW

```
Hardware Setup:
  ├── ESP32 USB → PC USB
  ├── LED (GPIO 25) + 220Ω → GND
  ├── Relay (GPIO 2) + External 5V → GND
  └── Webcam USB (optional, untuk face recognition)

Arduino Upload:
  ├── Open: testbukapintu_serial_usb.ino
  ├── Board: ESP32 Dev Module
  ├── Port: COM3
  └── Upload

Python Setup:
  ├── Install: pip install flask pyserial
  ├── Run: python test_esp32_web.py
  └── Browser: http://127.0.0.1:5000

Testing:
  ├── Check status indicator 🟢
  ├── Test LED 💡
  ├── Test Relay ⚡
  ├── Test Buka Pintu 🔓
  └── Verify hardware response
```

---

## 🎯 USE CASES

### 1. Development Testing
```
Gunakan untuk quick test setiap fitur
tanpa perlu membuka Serial Monitor di Arduino IDE
```

### 2. Hardware Debugging
```
Test LED dan Relay terpisah untuk diagnosa masalah hardware
```

### 3. End-to-End Integration Test
```
Test full door control workflow sebelum deploy
```

### 4. Demo/Presentation
```
Show working system kepada stakeholder via web interface
```

---

## 🚀 NEXT STEPS

1. ✅ Test dengan ini dulu
2. ✅ Verify LED dan Relay working
3. ✅ Verify door control working
4. ✅ Upgrade ke app_usb.py (dengan face recognition)
5. ✅ Deploy to production

---

## 📞 SUPPORT

- **Arduino Docs**: https://docs.esp32.dev
- **Pyserial Docs**: https://pyserial.readthedocs.io
- **Flask Docs**: https://flask.palletsprojects.com

---

## 🎉 READY TO TEST!

```
python test_esp32_web.py
→ http://127.0.0.1:5000
→ Start testing! 🚀
```

**Happy testing!** 🎯

