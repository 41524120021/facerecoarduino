# 🎉 FITUR BARU: LED BERKEDIP + RELAY TERUS BUNYI

Implementasi lengkap untuk membuat pintu lebih meriah saat terbuka!

---

## 📦 FILE YANG TERSEDIA

### 1️⃣ **testbukapintu_serial_usb.ino** (ORIGINAL - DISIMPAN)
- LED: ON terus selama 10 detik
- Relay: ON terus selama 10 detik
- Sederhana, stabil, tested

### 2️⃣ **testbukapintu_serial_usb_blinking.ino** ⭐ (BARU - RECOMMENDED)
- ✨ LED: **BERKEDIP 300ms** (ON/OFF/ON/OFF...)
- 📣 Relay: **PULSING 500ms** (ON/OFF/ON/OFF...)
- Lebih menarik, LED berkedip selama pintu buka 10 detik
- Relay bunyi pulsing (bukan terus menerus)

### 3️⃣ **testbukapintu_serial_usb_rgb.ino** 🌈 (BARU - RGB LED)
- 🌈 LED: **WARNA WARNI** (berubah setiap 500ms)
- 📣 Relay: **PULSING 500ms**
- Untuk RGB LED (3 pin: Red, Green, Blue)
- Rainbow effect - paling meriah!

---

## 🎯 PILIHAN MANA?

### Untuk Single Color LED:
```
Kabel:
  LED Anode → GPIO 25 + Resistor 220Ω
  LED Katode → GND

Gunakan: testbukapintu_serial_usb_blinking.ino
```

### Untuk RGB LED:
```
Kabel:
  LED Red   → GPIO 25
  LED Green → GPIO 26  
  LED Blue  → GPIO 27
  GND → GND

Gunakan: testbukapintu_serial_usb_rgb.ino
```

---

## 💾 CARA UPLOAD

### Step 1: Pilih Sketch
```
Arduino IDE → File → Open

Pilih salah satu:
  ✓ testbukapintu_serial_usb_blinking.ino    (Single LED)
  ✓ testbukapintu_serial_usb_rgb.ino         (RGB LED)
```

### Step 2: Atur Board & Port
```
Tools → Board → ESP32 Dev Module
Tools → Port → COM3 (atau port Anda)
```

### Step 3: Upload
```
Sketch → Upload (Ctrl+U)
```

### Step 4: Test via Serial Monitor
```
Tools → Serial Monitor (Ctrl+Shift+M)
Baud: 115200

Ketik: pintu=BUKA
```

---

## ⚙️ TIMING CONFIGURATION

### LED Blinking (Single Color Version)
```cpp
const unsigned long BLINK_INTERVAL = 300;    // 300ms = fast kedip
```

Ubah untuk kecepatan berbeda:
- `100ms` - Sangat cepat (strobe effect)
- `300ms` - Cepat (medium speed) ← Default
- `500ms` - Normal (medium speed)
- `1000ms` - Lambat (2 kedip/detik)

### Relay Pulsing
```cpp
const unsigned long RELAY_PULSE = 500;       // 500ms = ON 250ms, OFF 250ms
```

Ubah untuk bunyi berbeda:
- `200ms` - Cepat (bunyi cepat)
- `500ms` - Medium (default)
- `1000ms` - Lambat (bunyi lambat)

### Door Duration (sama di semua version)
```cpp
const unsigned long DOOR_DURATION = 10000;   // 10 detik
```

Ubah untuk durasi berbeda:
- `5000` - 5 detik
- `10000` - 10 detik (default)
- `15000` - 15 detik
- `20000` - 20 detik

---

## 🌈 RGB WARNA-WARNI REFERENCE

### RGB Warna Dasar
```cpp
Merah:       setRGB(255, 0, 0)
Hijau:       setRGB(0, 255, 0)
Biru:        setRGB(0, 0, 255)
```

### RGB Warna Mix
```cpp
Kuning:      setRGB(255, 255, 0)     // Red + Green
Cyan:        setRGB(0, 255, 255)     // Green + Blue
Magenta:     setRGB(255, 0, 255)     // Red + Blue
Putih:       setRGB(255, 255, 255)   // Red + Green + Blue
```

### RGB Warna Special
```cpp
Orange:      setRGB(255, 165, 0)
Pink:        setRGB(255, 192, 203)
Purple:      setRGB(128, 0, 128)
Brown:       setRGB(165, 42, 42)
```

---

## 🎨 CUSTOM RGB WARNA

Edit array `colors[]` di sketch:

```cpp
// Default: 7 warna rainbow
const RGB colors[] = {
  {255, 0, 0},      // Merah
  {255, 127, 0},    // Orange
  {255, 255, 0},    // Kuning
  {0, 255, 0},      // Hijau
  {0, 255, 255},    // Cyan
  {0, 0, 255},      // Biru
  {255, 0, 255},    // Magenta
};

// Atau customize dengan warna favorit:
const RGB colors[] = {
  {255, 0, 0},      // Merah (company primary color)
  {0, 0, 255},      // Biru (company secondary color)
  {255, 255, 0},    // Kuning (accent)
};
```

Setiap warna akan berganti setiap `COLOR_CHANGE` ms (default 500ms).

---

## 📊 COMMAND REFERENCE

### All Versions Support These:

```
pintu=BUKA      → Buka pintu 10 detik (LED kedip/warna + Relay pulsing)
pintu=TUTUP     → Tutup pintu immediate
test=LED        → Test LED
test=RELAY      → Test Relay pulsing 2 detik
status          → Get current status
```

### Response Examples:

**When BUKA:**
```
🔓 BUKA PINTU!
💡 LED berkedip + 📣 RELAY pulsing (10 detik)

[output setiap 50ms]:
🔊.🔊.🔊.🔊.🔊.🔊.🔊. ... (10 detik)

💡 LED OFF
📣 RELAY OFF
✅ SELESAI
```

**When test=LED (single color):**
```
💡 TEST LED - Blink 3x
✓✓✓
✅ LED test selesai
```

**When test=LED (RGB):**
```
🌈 TEST RGB - Tampilkan semua warna
  🔴 Merah
  🟠 Orange
  🟡 Kuning
  🟢 Hijau
  🔵 Cyan
  🔵 Biru
  🟣 Magenta
✅ RGB test selesai
```

---

## 🔧 HARDWARE SETUP

### Single Color LED Setup:
```
ESP32 GPIO 25 ──┬─→ [220Ω Resistor] ─→ LED Anode (+)
                └─→ GND ← LED Katode (-)

ESP32 GPIO 2 ──→ Relay Signal
GND ────────→ Relay GND
5V (external) ─→ Relay 5V Power
```

### RGB LED Setup:
```
ESP32 GPIO 25 ──→ [220Ω] ──→ Red LED Anode
ESP32 GPIO 26 ──→ [220Ω] ──→ Green LED Anode
ESP32 GPIO 27 ──→ [220Ω] ──→ Blue LED Anode
ESP32 GND ────→ RGB LED Common Cathode

ESP32 GPIO 2 ──→ Relay Signal
GND ────────→ Relay GND
5V (external) ─→ Relay 5V Power
```

---

## 🧪 TESTING GUIDE

### Test 1: Connection
```bash
python test_esp32_serial.py
→ Menu → 1. Test Connection
```

### Test 2: LED
```bash
# Via Serial Monitor (115200 baud):
test=LED
[LED harus berkedip/berubah warna]
```

### Test 3: Relay
```bash
# Via Serial Monitor:
test=RELAY
[Relay harus pulse/bunyi 2 detik]
```

### Test 4: Full Door Control
```bash
# Via Python:
from esp32_serial import ESP32SerialController

esp32 = ESP32SerialController("COM3", 115200)
esp32.open()
esp32.send_command("pintu=BUKA")
# Lihat LED berkedip + Relay pulsing selama 10 detik
esp32.close()

# Atau via web interface:
# http://localhost:5000 → Klik "🔓 Buka Pintu"
```

---

## 📋 PERBANDINGAN 3 VERSION

| Feature | Original | Blinking | RGB |
|---------|----------|----------|-----|
| **LED** | Terus ON | Berkedip | Warna-warni |
| **Relay** | Terus ON | Pulsing | Pulsing |
| **Hardware** | 1 LED | 1 LED | 3 LED (RGB) |
| **Kompleksitas** | Simple | Medium | Medium |
| **Kemeriahannya** | ⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Setup Time** | 5 min | 5 min | 10 min |

---

## ⚡ QUICK START

### Option 1: Single Color LED (RECOMMENDED FOR SIMPLICITY)
```
1. Wire LED to GPIO 25 + Resistor
2. Wire Relay to GPIO 2
3. Upload: testbukapintu_serial_usb_blinking.ino
4. Test: pintu=BUKA
```

### Option 2: RGB LED (MOST FUN)
```
1. Wire 3 LED (RGB) to GPIO 25, 26, 27
2. Wire Relay to GPIO 2
3. Upload: testbukapintu_serial_usb_rgb.ino
4. Test: pintu=BUKA
```

---

## 🎯 CUSTOMIZATION IDEAS

### Idea 1: Company Colors
```cpp
// Update colors[] dengan company colors
const RGB colors[] = {
  {255, 0, 0},      // Brand red
  {0, 0, 255},      // Brand blue
};
```

### Idea 2: Department-Specific
```cpp
// CEO office → Gold
// Manager → Blue
// Staff → Green
```

### Idea 3: Time-Based
```cpp
// Morning (8-12) → Green (ready)
// Afternoon (12-17) → Yellow (working)
// Evening (17-19) → Orange (ending)
// Night (19-8) → Red (closed)
```

### Idea 4: Multiple Speeds
```
test=LED       → Normal speed
test=LED_FAST  → Cepat
test=LED_SLOW  → Lambat
```

---

## 📞 TROUBLESHOOTING

| Problem | Solution |
|---------|----------|
| LED tidak berkedip | Check GPIO 25 wiring + resistor |
| LED berkedip tapi dim | Raise resistor value atau reduce PWM |
| Relay tidak bunyi | Check GPIO 2 wiring + external power |
| RGB hanya 1 warna | Check GPIO 26, 27 wiring |
| Serial error | Cek baud rate 115200 di Serial Monitor |
| Pintu tidak auto-close | Check DOOR_DURATION value |

---

## 🚀 NEXT STEPS

1. ✅ Upload salah satu sketch
2. ✅ Test via Serial Monitor
3. ✅ Test via web interface (http://localhost:5000)
4. ✅ Customize timing/colors sesuai preferensi
5. ✅ Deploy to production!

---

**Pilih version favorit dan upload sekarang!** 🎉

