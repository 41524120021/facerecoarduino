# 🔓 ESP32 Door Control System

Sistem otomatis pembuka pintu menggunakan ESP32 yang terhubung dengan Face Recognition system via MQTT.

## 📋 File-File

| File | Deskripsi |
|------|-----------|
| **esp32_door_control.ino** | Script utama ESP32 (upload ke board) |
| **esp32_debug_testing.ino** | Script testing & troubleshooting |
| **PANDUAN_ESP32.md** | Dokumentasi instalasi lengkap |
| **ESP32_QUICK_REFERENCE.h** | Quick reference & tips |

---

## ⚡ Quick Start (5 Menit)

### 1️⃣ Hardware Setup
```
ESP32 GPIO 25  → LED + (via resistor 220Ω)
ESP32 GPIO 2   → Relay IN (sinyal)
ESP32 GND      → LED- & Relay GND
ESP32 5V/3.3V  → Relay VCC (dari power eksternal 5V)
Relay Output   → Buzzer/Solenoid Lock
```

### 2️⃣ Arduino IDE Setup
- Install [Arduino IDE](https://www.arduino.cc/en/software)
- Tools → Board Manager → Install "esp32"
- Sketch → Include Library → Install "PubSubClient"

### 3️⃣ Konfigurasi
Edit `esp32_door_control.ino` baris 41-42:
```cpp
const char* ssid = "NAMA_WIFI_ANDA";
const char* password = "PASSWORD_WIFI_ANDA";
```

### 4️⃣ Upload
- Tools → Board → DOIT ESP32 DEVKIT V1
- Tools → Port → Pilih COM port
- Sketch → Upload

### 5️⃣ Test
- Tools → Serial Monitor (Baud: 115200)
- Lihat: `✅ WIFI Terhubung!` dan `✅ Connected!`

---

## 🔌 Wiring Diagram

```
┌─────────────────────────────────────────┐
│           ESP32 DEVKIT V1               │
│                                         │
│  GPIO 25  ──→ LED+ (220Ω) ──→ LED     │
│  GND      ──→ LED-                     │
│                                         │
│  GPIO 2   ──→ Relay IN                 │
│  5V*      ──→ Relay VCC (*external)    │
│  GND      ──→ Relay GND                │
│                                         │
└─────────────────────────────────────────┘

Relay Output:
  COM ──→ Buzzer/Solenoid (+)
  NO  ──→ Power Supply (-)
  GND ──→ Ground
```

---

## 📡 MQTT Protocol

**Broker:** `broker.hivemq.com:1883`  
**Topic:** `fc/pintu`

### Pesan yang Didukung

| Pesan | Aksi |
|-------|------|
| `pintu=BUKA` | LED ON + Relay ON (10 detik) |
| `pintu=TUTUP` | LED OFF + Relay OFF (instant) |
| `test=LED` | LED blink 1x (debug) |
| `test=RELAY` | Relay ON 2 detik (debug) |

---

## 🚀 Integrasi dengan Face Recognition

Alur kerja:
```
1. User klik "Buka Pintu" di web
   ↓
2. Flask publish MQTT: "pintu=BUKA"
   ↓
3. ESP32 terima → LED ON, Relay ON (10 detik)
   ↓
4. Flask publish MQTT: "pintu=TUTUP"
   ↓
5. ESP32 terima → LED OFF, Relay OFF
```

---

## 🧪 Testing

### Cara 1: Serial Monitor
```
Upload esp32_door_control.ino
→ Buka Serial Monitor (115200)
→ Amati output untuk WiFi/MQTT status
```

### Cara 2: Debug Script
```
Upload esp32_debug_testing.ino
→ Serial Monitor akan menampilkan menu
→ Pilih test (1-6)
```

### Cara 3: MQTT Client
```bash
# Subscribe
mosquitto_sub -h broker.hivemq.com -t fc/pintu

# Test
mosquitto_pub -h broker.hivemq.com -t fc/pintu -m "test=LED"
mosquitto_pub -h broker.hivemq.com -t fc/pintu -m "pintu=BUKA"
```

---

## ❌ Troubleshooting

| Problem | Solusi |
|---------|--------|
| WiFi tidak connect | Cek SSID/password, pastikan 2.4GHz WiFi |
| MQTT tidak connect | Pastikan WiFi sudah connect, cek internet |
| LED tidak menyala | Cek GPIO 25, polarity LED, resistor 220Ω |
| Relay tidak aktif | Cek GPIO 2, gunakan 5V eksternal, bukan 3.3V |
| Serial Monitor blank | Cek USB cable, port COM, driver CH340 |

Lihat `PANDUAN_ESP32.md` untuk troubleshooting lengkap.

---

## 📊 Pin Configuration

```cpp
const int LED_PIN = 25;      // GPIO 25 (LED indicator)
const int RELAY_PIN = 2;     // GPIO 2 (Relay/Buzzer)
```

Jika ingin ganti pin:
- Ubah nilai konstanta di bagian atas script
- Pastikan pin yang dipilih tidak conflict dengan onboard functions

---

## 🎯 Serial Monitor Output

```
✅ WIFI Terhubung!
✅ Subscribe ke topik: fc/pintu

[Saat ada pesan MQTT]
📡 MQTT Terima: fc/pintu → pintu=BUKA
🔓 BUKA PINTU!
💡 LED ON
📣 RELAY ON (Buzzer bunyi)

[10 detik kemudian]
💡 LED OFF
📣 RELAY OFF (Buzzer diam)
```

---

## 📚 Dokumentasi Lengkap

- **PANDUAN_ESP32.md** - Setup detail, wiring, troubleshooting
- **ESP32_QUICK_REFERENCE.h** - Quick tips, commands, alur kerja
- **esp32_debug_testing.ino** - Interactive testing suite

---

## 🔧 Perubahan Konfigurasi

### Ubah durasi LED/Relay (default 10 detik)
Edit `backend/app.py` baris 143:
```python
time.sleep(10)  # Ubah ke berapa saja (dalam detik)
```

### Ubah MQTT topic
Di `esp32_door_control.ino`:
```cpp
const char* mqtt_topic = "fc/pintu";  // Ubah ke topic baru
```

Pastikan Flask backend (`app.py`) juga menggunakan topic yang sama.

### Ubah pin LED/Relay
```cpp
const int LED_PIN = 25;      // Ubah GPIO
const int RELAY_PIN = 2;     // Ubah GPIO
```

---

## 🛠️ Hardware Requirements

| Item | Qty | Notes |
|------|-----|-------|
| ESP32 DEVKIT V1 | 1 | Atau clone yang compatible |
| LED (biru/merah) | 1 | 5mm atau 3mm |
| Resistor 220Ω | 1 | Untuk LED current limiting |
| Relay Module | 1 | 5V, single channel |
| Buzzer/Solenoid | 1 | 5V-12V sesuai relay |
| USB Cable | 1 | Data cable (bukan charge-only) |
| Power Supply | 1 | 5V 2A+ untuk relay |

---

## 📖 Dokumentasi Referensi

- [Arduino IDE Guide](https://www.arduino.cc/en/Guide)
- [ESP32 Docs](https://docs.espressif.com/projects/esp-idf/)
- [PubSubClient Library](https://github.com/knolleary/pubsubclient)
- [MQTT Protocol](https://mqtt.org/)

---

## 📱 Aplikasi Terkait

- **Frontend:** `frontend/face-recognition.html` (button "Buka Pintu")
- **Backend:** `backend/app.py` (route `/buka_pintu`, publish MQTT)
- **Database:** `php/karyawan/` (employee management)

---

## ✅ Checklist Persiapan

- [ ] Hardware sudah disiapkan (LED, Relay, USB cable)
- [ ] Arduino IDE terinstall
- [ ] ESP32 board ditambahkan ke Arduino IDE
- [ ] PubSubClient library terinstall
- [ ] WiFi credentials sudah di-update di script
- [ ] ESP32 sudah ter-upload dengan script ini
- [ ] Serial Monitor menunjukkan WiFi connected
- [ ] MQTT subscription berhasil
- [ ] Flask backend sudah running
- [ ] Siap testing

---

## 📞 Support

Jika ada error:
1. Lihat Serial Monitor output (baud 115200)
2. Lihat `PANDUAN_ESP32.md` untuk troubleshooting
3. Coba debug script: `esp32_debug_testing.ino`
4. Check wiring diagram di bagian atas

---

**Last Update:** Oktober 28, 2025  
**Author:** Face Recognition System  
**Version:** 1.0
