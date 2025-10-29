# ESP32 HARDWARE DEBUGGING CHECKLIST

## PHYSICAL COMPONENTS

### 1. LED (GPIO 25, 26, 27)
- **Lokasi:** Lihat physical ESP32 board
- **GPIO 25 (Merah):** Pin 25
- **GPIO 26 (Hijau):** Pin 26
- **GPIO 27 (Biru):** Pin 27
- **GND:** Pin GND
- **220Ω Resistor:** Setiap LED punya resistor?

❌ **Troubleshoot jika LED tidak hidup:**
1. Cek kabel dari GPIO ke LED (+) dan ke GND (-)
2. Cek resistor tidak putus
3. Cek LED polaritas (panjang = +, pendek = -)
4. Test resistor dengan multimeter (harus ≈220Ω)
5. Test LED dengan direct 3.3V battery

### 2. RELAY (GPIO 2)
- **Lokasi:** Pin 2 (Output)
- **Power Supply:** 5V external
- **Relay Module:** Apakah sudah connected?
- **Speaker/Buzzer:** Connected ke relay?

❌ **Troubleshoot jika relay tidak bunyi:**
1. Cek relay module power (5V + GND)
2. Cek GPIO 2 terhubung ke relay input
3. Cek speaker/buzzer di relay output
4. Test relay dengan direct 5V
5. Cek relay coil tidak rusak

### 3. DOOR MECHANISM
- **Solenoid/Motor:** Apakah sudah connected?
- **Power Supply:** 5V atau 12V (sesuai spec)?
- **Via Relay:** Kontrol via relay switch?

❌ **Troubleshoot jika door tidak bergerak:**
1. Test motor/solenoid dengan direct power
2. Cek relay switch membuka/menutup (dengarkan click)
3. Cek power supply amps cukup (min 1-2A untuk motor)
4. Cek kabel solenoid tersambung dengan benar

---

## SERIAL COMMUNICATION

Serial output yang kami dapat:
```
✅ PIN Setup: RGB LED (GPIO 25,26,27) + RELAY (GPIO 2)
📡 Terima: test=LED
  🔴 Merah
📡 Terima: test=RELAY
⚡ TEST RELAY - Pulse 2 detik
```

**Ini artinya:**
- ✅ Sketch sudah ter-upload dengan benar
- ✅ Serial communication bekerja
- ✅ ESP32 merespons perintah
- ✅ GPIO sudah set-up di firmware

**Tapi LED/Relay output mungkin:**
- Belum di-check fisik
- Atau kabel belum tersambung
- Atau hardware issue pada LED/Relay

---

## NEXT STEPS

### Step 1: Test dengan Serial Monitor
```
1. Buka Arduino IDE
2. Tools > Serial Monitor
3. Baud: 115200
4. Send: test=LED
5. Watch serial output + lihat LED berubah
```

### Step 2: Check PIN dengan Multimeter
```
1. Set multimeter ke DC voltage
2. Probe GPIO 25 → GND (saat test=LED)
3. Harus naik dari 0V ke 3.3V (LED ON)
```

### Step 3: Check dengan Oscilloscope
```
- PWM signal di GPIO 25/26/27 (test=LED)
- GPIO 2 pulse (test=RELAY)
```

### Step 4: Test Component Isolated
```
1. Disconnect dari board
2. Test LED dengan 3.3V battery
3. Test relay dengan 5V power supply
4. Test solenoid dengan appropriate voltage
```

---

## ALTERNATIVE FIXES

Jika LED/Relay tetap tidak bekerja:

### Option 1: Check Sketch
```
- Verify GPIO numbers di sketch
- Verify PWM duty cycle
- Verify timing logic
```

### Option 2: Check Wiring
```
- Redraw schematic
- Recheck semua connection
- Use ohmmeter test kabel
```

### Option 3: Try Simpler Sketch
```
- Buat sketch yang hanya test GPIO 25
- Buat sketch yang hanya test GPIO 2
- Verify masing-masing working
```

---

## SUGGESTED DIAGNOSTIC SCRIPT

```python
# Buat script yang test setiap GPIO individually
# GPIO 25 ON/OFF
# GPIO 26 ON/OFF
# GPIO 27 ON/OFF
# GPIO 2 ON/OFF

# Monitor response
# Measure voltage
# Listen for relay
```

---

## SERIAL OUTPUT INTERPRETATION

```
ESP32 Boot:
  rst:0x1 (POWERON_RESET)      ← Normal startup
  boot:0x13 (SPI_FAST_FLASH_BOOT) ← Sketch mode
  ✅ PIN Setup: ...             ← Setup success
  
Command Processing:
  📡 Terima: test=LED           ← Command received
  🌈 TEST RGB - Tampilkan...   ← Processing
  🔴 Merah                      ← Executing
  
Expected behavior:
  - Serial output = OK
  - GPIO voltage = should change
  - Physical output = LED on/relay click
```

---

## NEXT ACTION

1. **Check physical wiring** (most likely culprit)
2. **Verify component power supply** (LED 3.3V, Relay 5V)
3. **Test with simple code** (one GPIO at a time)
4. **Measure voltages** with multimeter

Kalau semua semuanya sudah benar, GPIO output bekerja tetapi LED/Relay tidak, 
maka masalah ada di component atau wiring, bukan sketch/firmware.
