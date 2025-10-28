# 📱 ESP32 Door Control System - Panduan Instalasi & Konfigurasi

## 🎯 Ringkasan Fitur

Script Arduino ESP32 ini mengontrol:
- **LED** (GPIO 25) - Indikator pintu terbuka
- **Relay** (GPIO 2) - Kontrol buzzer/solenoid lock
- **MQTT** - Menerima perintah dari Flask backend
- **WiFi** - Koneksi ke broker HIVEMQ

### Alur Kerja:
```
User klik "Buka Pintu" di web
        ↓
Flask kirim MQTT: "pintu=BUKA"
        ↓
ESP32 terima & proses
        ↓
LED ON 💡 + Relay ON 📣 (10 detik)
        ↓
Otomatis OFF setelah 10 detik
```

---

## 📋 Persyaratan Hardware

| Komponen | GPIO | Fungsi |
|----------|------|--------|
| **LED** | GPIO 25 | Indikator pintu terbuka (warna biru/merah) |
| **Relay** | GPIO 2 | Kontrol solenoid/buzzer |
| **Buzzer/Solenoid** | Relay OUT | Alarm/penggerak pintu |
| **WiFi** | Onboard | Koneksi ke broker MQTT |

---

## 🔌 Wiring Diagram

### LED Connection:
```
ESP32 (GPIO 25) → Resistor 220Ω → LED+ (Anoda)
ESP32 (GND)     ————————————————→ LED- (Katoda)
```

### Relay Connection:
```
ESP32 (GPIO 2)  → Relay IN (Signal)
ESP32 (5V/3.3V) → Relay VCC
ESP32 (GND)     → Relay GND

Relay Coil Output (NO/COM) → Buzzer/Solenoid Lock
```

### Buzzer/Solenoid Connection:
```
Relay COM  → (+) Buzzer/Solenoid
Relay NO   → (-) Buzzer/Solenoid
GND        → (-) Power Supply
```

---

## 🚀 Langkah Instalasi Arduino IDE

### 1. Download Arduino IDE
- Unduh dari: https://www.arduino.cc/en/software
- Install di komputer Anda

### 2. Tambah Board Manager ESP32
```
Tools → Board Manager
Search: "esp32"
Install: "esp32 by Espressif Systems" (latest version)
```

### 3. Install Library PubSubClient
```
Sketch → Include Library → Manage Libraries
Search: "PubSubClient"
Install: "PubSubClient by Nick O'Leary"
```

### 4. Konfigurasi Board
```
Tools → Board → DOIT ESP32 DEVKIT V1
(Atau sesuaikan dengan ESP32 yang Anda gunakan)
```

---

## ⚙️ Konfigurasi Kode

### 1. Buka file: `esp32_door_control.ino`

### 2. Edit WiFi credentials (baris 41-42):
```cpp
const char* ssid = "NAMA_WIFI_ANDA";        // Ganti dengan SSID WiFi
const char* password = "PASSWORD_WIFI_ANDA"; // Ganti dengan password WiFi
```

**Contoh:**
```cpp
const char* ssid = "Rumah_WiFi";
const char* password = "pass123456";
```

### 3. Edit MQTT credentials (opsional - sudah benar):
```cpp
const char* mqtt_server = "broker.hivemq.com"; // Broker MQTT (publik)
const int mqtt_port = 1883;
const char* mqtt_topic = "fc/pintu";           // HARUS SAMA dengan app.py
const char* mqtt_id = "esp32_door_01";         // ID unik ESP32
```

### 4. Pin configuration (sudah benar):
```cpp
const int LED_PIN = 25;      // GPIO 25 untuk LED
const int RELAY_PIN = 2;     // GPIO 2 untuk Relay
```

---

## 📤 Upload ke ESP32

### 1. Hubungkan ESP32 ke Komputer via USB
- Gunakan kabel USB data (bukan charge only)
- Tunggu driver terinstall otomatis

### 2. Tentukan Port
```
Tools → Port → COMx (cek di Device Manager jika tidak terlihat)
```

### 3. Upload Sketch
```
Sketch → Upload (atau Ctrl + U)
```

### 4. Monitor Serial Output
```
Tools → Serial Monitor (atau Ctrl + Shift + M)
Pilih Baud Rate: 115200
```

**Output yang diharapkan:**
```
╔═══════════════════════════════════════════════════╗
║   ESP32 DOOR CONTROL SYSTEM - Face Recognition   ║
╚═══════════════════════════════════════════════════╝
✅ PIN Setup: LED (GPIO 25) dan RELAY (GPIO 2)
🔄 Menghubungkan ke WIFI: Rumah_WiFi
✅ WIFI Terhubung!
📍 IP Address: 192.168.x.x
🔄 Mencoba connect ke MQTT broker... ✅ Connected!
✅ Subscribe ke topik: fc/pintu
📡 Publish: status=ONLINE
```

---

## 🧪 Testing

### Test 1: LED
1. Buka MQTT client (contoh: MQTT.fx, Mosquitto client, atau online)
2. Connect ke: `broker.hivemq.com:1883`
3. Publish ke topic: `fc/pintu`
4. Payload: `test=LED`
5. Lihat di Serial Monitor & amati LED blink sekali

### Test 2: Relay
1. Publish ke topic: `fc/pintu`
2. Payload: `test=RELAY`
3. Relay akan hidup 2 detik (buzzer bunyi/solenoid actuat)
4. Lihat di Serial Monitor

### Test 3: Full Buka Pintu
1. Publish ke topic: `fc/pintu`
2. Payload: `pintu=BUKA`
3. LED ON 💡 + Relay ON 📣 selama 10 detik
4. Otomatis OFF setelah 10 detik

### Test 4: Tutup Pintu
1. Publish ke topic: `fc/pintu`
2. Payload: `pintu=TUTUP`
3. LED OFF + Relay OFF (immediate)

---

## 🔗 Integrasi dengan Flask Backend

File Flask sudah dikonfigurasi untuk kirim MQTT:

**File:** `backend/app.py` (route `/buka_pintu`)

```python
@app.route('/buka_pintu', methods=['POST'])
def buka_pintu():
    client = mqtt.Client()
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    
    # Kirim BUKA
    client.publish(MQTT_TOPIC, "pintu=BUKA")
    
    # Tunggu 10 detik
    time.sleep(10)
    
    # Kirim TUTUP
    client.publish(MQTT_TOPIC, "pintu=TUTUP")
    
    client.disconnect()
    return {"status": "OK", "pesan": "pintu dibuka 10 detik"}
```

**Alur:**
1. User klik button "Buka Pintu" di halaman face recognition
2. JavaScript POST ke: `http://127.0.0.1:5000/buka_pintu`
3. Flask publish MQTT: "pintu=BUKA" ke broker
4. ESP32 terima & buka pintu (LED + Relay ON)
5. 10 detik kemudian Flask publish: "pintu=TUTUP"
6. ESP32 tutup pintu (LED + Relay OFF)

---

## 🐛 Troubleshooting

### Masalah: ESP32 tidak bisa upload
**Solusi:**
1. Cek apakah driver USB terinstall
2. Coba kabel USB yang berbeda
3. Coba port COM yang berbeda di Arduino IDE
4. Hold tombol "BOOT" saat upload

### Masalah: WiFi tidak terkoneksi
**Solusi:**
1. Cek SSID dan password (case-sensitive)
2. Pastikan 2.4GHz WiFi (ESP32 tidak support 5GHz)
3. Pastikan WiFi bisa access internet

### Masalah: MQTT tidak connect
**Solusi:**
1. Cek koneksi internet ESP32
2. Cek apakah broker `broker.hivemq.com` online
3. Lihat di Serial Monitor error message-nya
4. Coba restart ESP32

### Masalah: LED tidak menyala
**Solusi:**
1. Cek koneksi GPIO 25 → LED
2. Cek LED polarity (panjang = +, pendek = -)
3. Test dengan code debug: buat loop LED blink di setup()

### Masalah: Relay tidak bekerja
**Solusi:**
1. Cek koneksi GPIO 2 → Relay IN
2. Cek power relay (5V/3.3V + GND)
3. Gunakan external power supply untuk relay (tidak dari ESP32)
4. Test relay dengan multimeter

---

## 📊 Serial Monitor Output Reference

```
✅ PIN Setup: LED (GPIO 25) dan RELAY (GPIO 2)
   → Semua pin sudah disiapkan

🔄 Menghubungkan ke WIFI: Rumah_WiFi
   → ESP32 mencoba connect ke WiFi

✅ WIFI Terhubung!
   → WiFi berhasil

📍 IP Address: 192.168.1.100
   → IP yang diberikan router

🔄 Mencoba connect ke MQTT broker...
   → Sedang connect ke broker HIVEMQ

✅ Connected!
   → MQTT berhasil connect

✅ Subscribe ke topik: fc/pintu
   → Subscribe sudah aktif, siap terima pesan

📡 MQTT Terima: fc/pintu → pintu=BUKA
   → Pesan dari Flask diterima

🔓 BUKA PINTU!
   → Memproses perintah buka

💡 LED ON
📣 RELAY ON (Buzzer bunyi)
   → Aktuator hidup

(tunggu 10 detik)

💡 LED OFF
📣 RELAY OFF (Buzzer diam)
   → Aktuator mati setelah 10 detik
```

---

## 💾 File Lokasi

```
d:\xampp\htdocs\facereconigtion\
├── backend\
│   ├── app.py                    ← Flask backend (sudah konfigurasi MQTT)
│   ├── esp32_door_control.ino   ← Script ESP32 (FILE INI)
│   └── requirements.txt
├── frontend\
│   ├── face-recognition.html    ← Button "Buka Pintu" di sini
│   └── css\
│       └── global.css
└── php\
    └── admin\
        └── login.php
```

---

## ✅ Checklist Sebelum Testing

- [ ] Arduino IDE sudah terinstall
- [ ] Board ESP32 sudah ditambahkan ke Arduino IDE
- [ ] Library PubSubClient sudah terinstall
- [ ] SSID dan Password WiFi sudah diubah di kode
- [ ] LED sudah terhubung ke GPIO 25
- [ ] Relay sudah terhubung ke GPIO 2
- [ ] ESP32 sudah terupload dengan script ini
- [ ] Serial Monitor menunjukkan "✅ Connected!" dan subscribe berhasil
- [ ] Flask backend (`app.py`) sudah running
- [ ] Tombol "Buka Pintu" sudah tersedia di halaman face recognition

---

## 📧 Support & Tips

### Menggunakan MQTT Client untuk Testing:

**Opsi 1: MQTT.fx (Windows)**
- Download: http://www.jensd.de/apps/mqttfx/1.7.1/
- Connect: `broker.hivemq.com:1883`
- Subscribe: `fc/pintu`
- Publish: `pintu=BUKA`

**Opsi 2: Mosquitto (CLI)**
```bash
# Test subscribe
mosquitto_sub -h broker.hivemq.com -t fc/pintu

# Test publish
mosquitto_pub -h broker.hivemq.com -t fc/pintu -m "pintu=BUKA"
```

**Opsi 3: Online MQTT Client**
- Buka: http://www.hivemq.com/demos/websocket-client/
- Broker: `broker.hivemq.com`
- Port: `8000`

---

## 🎓 Konsep yang Digunakan

1. **MQTT** - Message Broker untuk komunikasi IoT
2. **WiFi** - Koneksi internet ESP32
3. **GPIO** - Kontrol digital output (LED, Relay)
4. **PubSubClient** - Library MQTT untuk Arduino
5. **Callback** - Fungsi untuk terima pesan MQTT
6. **Non-blocking Code** - ESP32 loop tidak freeze saat tunggu

---

**Dibuat untuk: Face Recognition Attendance System**
**Update: Oktober 28, 2025**
