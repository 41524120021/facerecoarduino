# 🚀 USB SERIAL QUICK START GUIDE

## Apa Bedanya USB Serial vs MQTT?

| Fitur | USB Serial | MQTT |
|-------|-----------|------|
| **Kecepatan** | ⚡ INSTANT (< 100ms) | 🐢 Lambat (1-2 detik) |
| **Setup** | 📱 Mudah (5 menit) | 🔧 Kompleks |
| **Jarak** | 📏 5 meter max (USB) | 🌐 Unlimited (Internet) |
| **Performa** | 🔥 Stabil | ⚠️ Tergantung broker |

**USB Serial REKOMENDASI untuk kantor lokal!**

---

## ⚡ 5 MENIT SETUP

### 1️⃣ Hardware Setup (1 menit)
```
ESP32 USB → PC USB
LED (GPIO 25) + Resistor 220Ω → GND
Relay (GPIO 2) + External 5V Power → GND
```

### 2️⃣ Upload Sketch (2 menit)
```
Arduino IDE:
- Open: testbukapintu_serial_usb.ino
- Board: ESP32 Dev Module
- Port: COM3 (atau port Anda)
- Upload (Ctrl+U)
```

### 3️⃣ Install Python Packages (1 menit)
```bash
cd backend
pip install -r requirements.txt
```

### 4️⃣ Run Application (1 menit)
```bash
python app_usb.py
# Buka browser: http://localhost:5000
```

**✅ SELESAI! Tombol "Buka Pintu" sudah siap!**

---

## 📋 Checklist

- [ ] ESP32 connected via USB
- [ ] LED + Resistor wired to GPIO 25
- [ ] Relay wired to GPIO 2 + External 5V power
- [ ] Arduino sketch uploaded successfully
- [ ] Python dependencies installed
- [ ] Flask app running
- [ ] Web interface accessible at http://localhost:5000
- [ ] ESP32 Status shows "✅ Terhubung"
- [ ] LED test works
- [ ] Relay test works
- [ ] Door control works

---

## 🛠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| COM port not found | Device Manager → Install CH340 driver |
| Permission denied | Close Serial Monitor, restart Flask |
| LED not lighting | Check GPIO 25 wiring + resistor |
| Relay not working | Check external 5V power supply connected |
| Face not detected | Add training photos to dataset/ folder |
| Web page won't load | Check Flask running + port 5000 free |

---

## 📚 Full Documentation

Lihat **SETUP_USB_SERIAL.md** untuk panduan lengkap dengan:
- ✅ Hardware wiring diagram detail
- ✅ Command reference
- ✅ Advanced troubleshooting
- ✅ Security notes

---

## 🎯 Next: Train Your Face Recognition

```bash
# Masukkan foto wajah ke folder:
dataset/
  └── nama_anda/
      ├── 1.jpg
      ├── 2.jpg
      └── 3.jpg

# Semakin banyak foto → Semakin akurat deteksi!
# Gunakan foto dari berbagai angle dan cahaya.
```

---

**Ready? Let's go! 🚀**

Questions? Check **SETUP_USB_SERIAL.md** for detailed guide.

