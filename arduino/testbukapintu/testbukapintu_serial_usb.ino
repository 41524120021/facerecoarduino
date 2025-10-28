// =============================================================
// ESP32 DOOR CONTROL SYSTEM - USB SERIAL VERSION
// =============================================================
// Fitur:
//   - Terima pesan dari USB Serial (bukan MQTT)
//   - Kontrol LED (pin 25) dan Relay (pin 2)
//   - Kecepatan: INSTANT (tidak perlu broker)
// 
// Koneksi Hardware:
//   - LED       → GPIO 25 (LED biru/merah)
//   - Relay     → GPIO 2  (Relay untuk buzzer/solenoid)
//   - USB       → Serial (untuk komunikasi dengan PC)
// 
// Kecepatan Serial: 115200 baud
// =============================================================

// ============================================================
// KONFIGURASI PIN
// ============================================================
const int LED_PIN = 25;                      // Pin LED
const int RELAY_PIN = 2;                     // Pin Relay (buzzer/solenoid)

// ============================================================
// SETUP
// ============================================================
void setup() {
  // Inisialisasi Serial Monitor (USB)
  Serial.begin(115200);
  delay(1000);
  
  Serial.println();
  Serial.println("╔═══════════════════════════════════════════════════╗");
  Serial.println("║   ESP32 DOOR CONTROL SYSTEM - USB SERIAL VERSION ║");
  Serial.println("╚═══════════════════════════════════════════════════╝");

  // Setup PIN
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // Matikan semua output di awal
  digitalWrite(LED_PIN, LOW);
  digitalWrite(RELAY_PIN, LOW);
  
  Serial.println("✅ PIN Setup: LED (GPIO 25) dan RELAY (GPIO 2)");
  Serial.println();
  Serial.println("📊 Konfigurasi:");
  Serial.println("   Mode: USB Serial (115200 baud)");
  Serial.println("   Siap menerima pesan via Serial");
  Serial.println();
  Serial.println("Pesan yang diterima:");
  Serial.println("   pintu=BUKA      → LED ON, Relay ON (10 detik)");
  Serial.println("   pintu=TUTUP     → LED OFF, Relay OFF");
  Serial.println("   test=LED        → LED blink 1x");
  Serial.println("   test=RELAY      → Relay ON 2 detik");
  Serial.println();
  Serial.println("─────────────────────────────────────────────────");
  Serial.println();
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  // Cek apakah ada data dari Serial (USB)
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();  // Hapus whitespace
    
    // Debug: tampilkan pesan yang diterima
    Serial.print("📡 Terima: ");
    Serial.println(message);

    // ========================================================
    // KONDISI 1: BUKA PINTU
    // ========================================================
    if (message == "pintu=BUKA") {
      Serial.println("🔓 BUKA PINTU!");
      
      // Nyalakan LED
      digitalWrite(LED_PIN, HIGH);
      Serial.println("💡 LED ON");
      
      // Nyalakan Relay (buzzer bunyi)
      digitalWrite(RELAY_PIN, HIGH);
      Serial.println("📣 RELAY ON (Buzzer bunyi)");
      
      // Tunggu 10 detik
      Serial.println("⏱️  Tunggu 10 detik...");
      delay(10000);
      
      // Matikan LED dan Relay (automatic)
      digitalWrite(LED_PIN, LOW);
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("💡 LED OFF");
      Serial.println("📣 RELAY OFF (Buzzer diam)");
      Serial.println("✅ SELESAI");
    }

    // ========================================================
    // KONDISI 2: TUTUP PINTU (IMMEDIATE)
    // ========================================================
    else if (message == "pintu=TUTUP") {
      Serial.println("🔒 TUTUP PINTU!");
      
      // Matikan LED dan Relay
      digitalWrite(LED_PIN, LOW);
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("💡 LED OFF");
      Serial.println("📣 RELAY OFF");
      Serial.println("✅ SELESAI");
    }

    // ========================================================
    // KONDISI 3: TEST LED
    // ========================================================
    else if (message == "test=LED") {
      Serial.println("🧪 Test LED...");
      digitalWrite(LED_PIN, HIGH);
      delay(1000);
      digitalWrite(LED_PIN, LOW);
      Serial.println("✅ Test LED selesai");
    }

    // ========================================================
    // KONDISI 4: TEST RELAY
    // ========================================================
    else if (message == "test=RELAY") {
      Serial.println("🧪 Test RELAY...");
      digitalWrite(RELAY_PIN, HIGH);
      delay(2000);
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("✅ Test RELAY selesai");
    }

    // ========================================================
    // STATUS LED & RELAY
    // ========================================================
    else if (message == "status") {
      Serial.println("📊 STATUS:");
      Serial.print("   LED: ");
      Serial.println(digitalRead(LED_PIN) ? "ON 💡" : "OFF");
      Serial.print("   RELAY: ");
      Serial.println(digitalRead(RELAY_PIN) ? "ON 📣" : "OFF");
    }

    // ========================================================
    // PESAN TIDAK DIKENAL
    // ========================================================
    else {
      Serial.print("❌ Pesan tidak dikenal: ");
      Serial.println(message);
      Serial.println("Gunakan: pintu=BUKA, pintu=TUTUP, test=LED, test=RELAY, status");
    }

    Serial.println();  // Blank line untuk readability
  }

  delay(10);  // Debounce
}

// =============================================================
// CATATAN INSTALASI:
// =============================================================
// 1. Upload sketch ini ke ESP32
// 2. Hubungkan ESP32 ke PC via USB
// 3. Buka Serial Monitor (115200 baud)
// 4. Kirim pesan:
//    - Ketik: pintu=BUKA
//    - Tekan: Enter
//    - LED dan Relay akan hidup 10 detik
//
// =============================================================
// KOMUNIKASI DENGAN PYTHON (Flask):
// =============================================================
// Gunakan library: pyserial
//
// import serial
// import time
//
// # Connect ke USB/Serial
// ser = serial.Serial('COM3', 115200, timeout=1)
// time.sleep(2)
//
// # Kirim pesan
// ser.write(b'pintu=BUKA\n')
//
// # Baca response
// response = ser.readline().decode('utf-8').strip()
// print(response)
//
// ser.close()
//
// =============================================================
// KONEKSI PIN HARDWARE:
// =============================================================
// ESP32      →  LED (Katode)
// GPIO 25    →  LED+ (Anoda via resistor 220Ω ke 5V/3.3V)
// GND        →  LED-
//
// ESP32      →  Relay
// GPIO 2     →  IN (Signal)
// 5V         →  VCC (+ Relay) - GUNAKAN POWER EKSTERNAL!
// GND        →  GND (- Relay)
//
// Relay OUT  →  Buzzer/Solenoid Lock
// =============================================================
