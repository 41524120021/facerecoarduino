// ═══════════════════════════════════════════════════════════════════
// ESP32 QUICK REFERENCE - FACE RECOGNITION DOOR SYSTEM
// ═══════════════════════════════════════════════════════════════════

/*
╔═══════════════════════════════════════════════════════════════════╗
║ ALUR KERJA SISTEM                                                 ║
╚═══════════════════════════════════════════════════════════════════╝

┌─────────────────────┐
│  User Interface     │
│  (Web Browser)      │
│                     │
│  - Klik "Buka Pintu"│
│  - LED menyala      │
│  - Relay/Buzzer ON  │
└──────────┬──────────┘
           │
           │ HTTP POST
           │ /buka_pintu
           ▼
┌─────────────────────┐
│  Flask Backend      │
│  (Python)           │
│  http://127.0.0.1   │
│  :5000              │
│                     │
│  - Generate MQTT    │
│  - Kirim "BUKA"     │
│  - Wait 10 detik    │
│  - Kirim "TUTUP"    │
└──────────┬──────────┘
           │
           │ MQTT Publish
           │ Topic: fc/pintu
           │ Broker: HiveMQ
           ▼
┌─────────────────────┐
│  ESP32 Receiver     │
│  (Arduino)          │
│                     │
│  - Terima "BUKA"    │
│  - LED GPIO 25 ON   │
│  - Relay GPIO 2 ON  │
│  - Buzzer/Lock ON   │
│                     │
│  [10 detik...]      │
│                     │
│  - Terima "TUTUP"   │
│  - LED GPIO 25 OFF  │
│  - Relay GPIO 2 OFF │
│  - Buzzer/Lock OFF  │
└─────────────────────┘

*/

// ═══════════════════════════════════════════════════════════════════
// 1. PIN CONFIGURATION
// ═══════════════════════════════════════════════════════════════════

/*
GPIO 25 ──→ LED+ (melalui resistor 220Ω)
GPIO 2  ──→ Relay IN (signal)
GND     ──→ LED- & Relay GND
5V/3.3V ──→ Relay VCC

Relay Output:
  COM ──→ Buzzer/Solenoid +
  NO  ──→ Power Supply -
  GND ──→ Power Supply -

*/

// ═══════════════════════════════════════════════════════════════════
// 2. LIBRARY & DEPENDENCIES
// ═══════════════════════════════════════════════════════════════════

/*
#include <WiFi.h>              // WiFi connectivity
#include <PubSubClient.h>      // MQTT client library

Install via Arduino IDE:
1. Sketch → Include Library → Manage Libraries
2. Search: "PubSubClient" by Nick O'Leary
3. Click Install

*/

// ═══════════════════════════════════════════════════════════════════
// 3. KONFIGURASI YANG PERLU DIUBAH
// ═══════════════════════════════════════════════════════════════════

/*
Line 41-42:
  const char* ssid = "NAMA_WIFI_ANDA";
  const char* password = "PASSWORD_WIFI_ANDA";

HARUS DISESUAIKAN dengan WiFi Anda!

Contoh:
  const char* ssid = "Rumah_WiFi";
  const char* password = "pass123456";

*/

// ═══════════════════════════════════════════════════════════════════
// 4. MQTT TOPICS & PAYLOADS
// ═══════════════════════════════════════════════════════════════════

/*
Topic:  fc/pintu
Broker: broker.hivemq.com:1883

Payloads yang didukung:
  ┌─────────────────┬──────────────────────────────────┐
  │ Payload         │ Aksi                             │
  ├─────────────────┼──────────────────────────────────┤
  │ pintu=BUKA      │ LED ON, Relay ON (10 detik)     │
  │ pintu=TUTUP     │ LED OFF, Relay OFF (immediate)  │
  │ test=LED        │ LED blink 1x (debug)            │
  │ test=RELAY      │ Relay ON 2 detik (debug)        │
  │ status=ONLINE   │ ESP32 online status             │
  │ DEBUG=...       │ Custom debug messages           │
  └─────────────────┴──────────────────────────────────┘

*/

// ═══════════════════════════════════════════════════════════════════
// 5. SERIAL OUTPUT INTERPRETATION
// ═══════════════════════════════════════════════════════════════════

/*
Output Expected:

✅ PIN Setup: LED (GPIO 25) dan RELAY (GPIO 2)
  → Pins sudah siap, tidak ada konflik

🔄 Menghubungkan ke WIFI: Rumah_WiFi
  → Sedang connect ke WiFi

✅ WIFI Terhubung!
  → WiFi sukses
   📍 IP Address: 192.168.1.100
  → IP yang diberikan router

🔄 Mencoba connect ke MQTT broker... ✅ Connected!
  → MQTT connect sukses

✅ Subscribe ke topik: fc/pintu
  → Siap menerima pesan MQTT

═══════════════════════════════════════════════════════════
STATUS MONITORING (setiap 30 detik):

⏰ Status LED: OFF
⏰ Status RELAY: OFF
📡 MQTT Connected: ✅ Yes
🌐 WIFI Signal: -45 (dBm, semakin tinggi semakin lemah)

═══════════════════════════════════════════════════════════
SAAT MENERIMA PESAN:

📡 MQTT Terima: fc/pintu → pintu=BUKA
  → Flask mengirim perintah BUKA

🔓 BUKA PINTU!
💡 LED ON
📣 RELAY ON (Buzzer bunyi)
  → LED & Relay menyala

(tunggu 10 detik)

💡 LED OFF
📣 RELAY OFF (Buzzer diam)
  → LED & Relay mati setelah 10 detik

*/

// ═══════════════════════════════════════════════════════════════════
// 6. TROUBLESHOOTING CHECKLIST
// ═══════════════════════════════════════════════════════════════════

/*
❌ WiFi tidak connect:
   ✓ Cek SSID & password (case-sensitive)
   ✓ WiFi harus 2.4GHz (ESP32 tidak support 5GHz)
   ✓ WiFi harus bisa akses internet
   ✓ Jaraknya terlalu jauh dari router?
   ✓ Coba restart router

❌ MQTT tidak connect:
   ✓ Pastikan WiFi sudah connect
   ✓ Cek broker status (broker.hivemq.com online?)
   ✓ Coba ping broker: ping broker.hivemq.com
   ✓ Cek firewall ESP32 (port 1883 open?)
   ✓ Lihat error code di Serial Monitor

❌ LED tidak menyala:
   ✓ Cek GPIO 25 ke LED+ sudah ter-solder?
   ✓ Resistor 220Ω sudah ada?
   ✓ LED polarity: panjang = +, pendek = -
   ✓ Coba blink test dengan code:
        digitalWrite(25, HIGH); delay(500); digitalWrite(25, LOW);
   ✓ Coba ganti LED baru

❌ Relay tidak aktif:
   ✓ Cek GPIO 2 ke Relay IN sudah ter-solder?
   ✓ Relay power supply (5V/3.3V + GND) terhubung?
   ✓ JANGAN gunakan 3.3V untuk relay, gunakan 5V eksternal!
   ✓ Test relay dengan multimeter (harus continuity saat ON)
   ✓ Coba relay yang berbeda

❌ Serial Monitor tidak tampil:
   ✓ Cek USB cable (pastikan data cable, bukan charging only)
   ✓ Cek Board: Tools → Board → DOIT ESP32 DEVKIT V1
   ✓ Cek Port: Tools → Port → COMx yang benar
   ✓ Coba port berbeda
   ✓ Update driver USB CH340 (untuk clone boards)

*/

// ═══════════════════════════════════════════════════════════════════
// 7. TESTING COMMANDS (via MQTT Client)
// ═══════════════════════════════════════════════════════════════════

/*
Tools untuk testing MQTT:
1. Arduino Serial Monitor → Lihat output
2. MQTT.fx → Publish/Subscribe test
3. Mosquitto → CLI testing
4. Online MQTT Client → http://www.hivemq.com/demos/websocket-client/

CLI Commands:

# Subscribe (terminal 1)
mosquitto_sub -h broker.hivemq.com -t fc/pintu

# Publish (terminal 2)
mosquitto_pub -h broker.hivemq.com -t fc/pintu -m "pintu=BUKA"
mosquitto_pub -h broker.hivemq.com -t fc/pintu -m "test=LED"
mosquitto_pub -h broker.hivemq.com -t fc/pintu -m "test=RELAY"

# Monitor all topics
mosquitto_sub -h broker.hivemq.com -t '#'

*/

// ═══════════════════════════════════════════════════════════════════
// 8. TIMING & DELAYS
// ═══════════════════════════════════════════════════════════════════

/*
Durasi LED/Relay saat "BUKA": 10 detik (hardcoded di app.py)

Di app.py:
  client.publish(MQTT_TOPIC, "pintu=BUKA")
  time.sleep(10)                            ← 10 detik
  client.publish(MQTT_TOPIC, "pintu=TUTUP")

Jika ingin ubah durasi:
  Line 143 di app.py: time.sleep(10) → ubah ke berapa saja
  Rekompile & push ke GitHub

*/

// ═══════════════════════════════════════════════════════════════════
// 9. HARDWARE WIRING DIAGRAM (ASCII)
// ═══════════════════════════════════════════════════════════════════

/*
┌─────────────────────────────────────────────────────────┐
│                      ESP32                              │
│     ┌────────────────────────────────────────────┐      │
│     │                                            │      │
│     │  VCC ──────→ 5V [External Power]          │      │
│     │  GND ──────→ GND                          │      │
│     │                                            │      │
│     │  GPIO 25 ──→ [220Ω Resistor] ──→ LED+   │      │
│     │  GND ──────→ LED-                         │      │
│     │                                            │      │
│     │  GPIO 2 ───→ Relay IN (Signal)           │      │
│     │  5V ───────→ Relay VCC (from PSU)        │      │
│     │  GND ──────→ Relay GND (from PSU)        │      │
│     │                                            │      │
│     │  [Relay Coil Output]                      │      │
│     │     COM ───→ Buzzer/Solenoid +           │      │
│     │     NO  ───→ Power Supply -               │      │
│     │                                            │      │
│     └────────────────────────────────────────────┘      │
│                                                         │
│                 USB (Upload)                           │
└─────────────────────────────────────────────────────────┘

Catatan Penting:
- GUNAKAN Power Supply EKSTERNAL untuk Relay (5V, minimal 2A)
- Relay tidak boleh diambil dari 3.3V ESP32
- Gunakan Common Ground (GND) untuk semua komponen

*/

// ═══════════════════════════════════════════════════════════════════
// 10. INTEGRATION FLOW
// ═══════════════════════════════════════════════════════════════════

/*
WEB BROWSER
  ↓
  User klik "Buka Pintu" button
  ↓
FRONTEND (JavaScript)
  ↓
  const response = await fetch(
    'http://127.0.0.1:5000/buka_pintu',
    { method: 'POST' }
  )
  ↓
FLASK BACKEND (app.py)
  ↓
  @app.route('/buka_pintu', methods=['POST'])
  def buka_pintu():
    client = mqtt.Client()
    client.connect('broker.hivemq.com', 1883, 60)
    
    # Kirim BUKA
    client.publish('fc/pintu', 'pintu=BUKA')
    
    # Tunggu 10 detik
    time.sleep(10)
    
    # Kirim TUTUP
    client.publish('fc/pintu', 'pintu=TUTUP')
    
    return {"status": "OK"}
  ↓
MQTT BROKER (hivemq.com)
  ↓
  Topic: fc/pintu
  Payload: pintu=BUKA
  ↓
ESP32 RECEIVER
  ↓
  mqtt_callback() triggered
  ↓
  if (message == "pintu=BUKA") {
    digitalWrite(LED_PIN, HIGH)    → LED ON
    digitalWrite(RELAY_PIN, HIGH)  → Relay ON
  }
  ↓
HARDWARE
  ↓
  LED MENYALA 💡
  RELAY/BUZZER AKTIF 📣
  ↓
  [10 detik kemudian...]
  ↓
  message == "pintu=TUTUP"
  ↓
  digitalWrite(LED_PIN, LOW)    → LED OFF
  digitalWrite(RELAY_PIN, LOW)  → Relay OFF
  ↓
  SELESAI ✓

*/

// ═══════════════════════════════════════════════════════════════════
// 11. MAINTENANCE & UPDATES
// ═══════════════════════════════════════════════════════════════════

/*
Backup:
  - Simpan esp32_door_control.ino di GitHub
  - Simpan WiFi credentials terpisah (tidak di publish)

Update:
  - Jika ada perubahan konfigurasi di app.py, update ESP32 sketch
  - Jika MQTT topic berubah, update di ESP32
  - Test di debug mode sebelum production

Monitoring:
  - Lihat Serial Monitor secara berkala
  - Check MQTT messages masuk/keluar
  - Monitor LED/Relay status setiap 30 detik
  - Alert jika WiFi/MQTT terputus

*/

// ═══════════════════════════════════════════════════════════════════
// 12. USEFUL LINKS
// ═══════════════════════════════════════════════════════════════════

/*
Arduino IDE Documentation:
  https://www.arduino.cc/en/Guide

ESP32 Documentation:
  https://docs.espressif.com/projects/esp-idf/

PubSubClient Library:
  https://github.com/knolleary/pubsubclient

HiveMQ Broker:
  https://www.hivemq.com/

MQTT Protocol:
  https://mqtt.org/

*/

// ═══════════════════════════════════════════════════════════════════
// QUICK COPY-PASTE COMMANDS
// ═══════════════════════════════════════════════════════════════════

/*
Test WiFi Connection:
  Serial Monitor harus tampil: ✅ WIFI Terhubung!

Test MQTT Connection:
  Serial Monitor harus tampil: ✅ Connected! + ✅ Subscribe ke topik

Test LED:
  Publish: fc/pintu → test=LED
  Harapan: LED blink 1x

Test Relay:
  Publish: fc/pintu → test=RELAY
  Harapan: Relay ON 2 detik (buzzer bunyi)

Full System:
  Publish: fc/pintu → pintu=BUKA
  Harapan: LED ON + Relay ON selama 10 detik
  Kemudian Flask otomatis publish: pintu=TUTUP
  Harapan: LED OFF + Relay OFF

*/

// ═══════════════════════════════════════════════════════════════════
// END OF QUICK REFERENCE
// ═══════════════════════════════════════════════════════════════════
