// =============================================================
// ESP32 DOOR CONTROL SYSTEM - USB SERIAL VERSION
// DENGAN FITUR LED BERKEDIP + RELAY TERUS BUNYI
// =============================================================
// Fitur:
//   - Terima pesan dari USB Serial (bukan MQTT)
//   - Kontrol LED (pin 25) - BERKEDIP SELAMA PINTU BUKA
//   - Kontrol Relay (pin 2) - TERUS BUNYI SELAMA PINTU BUKA
//   - Kecepatan: INSTANT (tidak perlu broker)
// 
// Koneksi Hardware:
//   - LED       → GPIO 25 (LED dengan resistor 220Ω)
//   - Relay     → GPIO 2  (Relay untuk buzzer/solenoid)
//   - USB       → Serial (untuk komunikasi dengan PC)
// 
// Kecepatan Serial: 115200 baud
// Durasi Pintu: 10 detik (LED berkedip + Relay bunyi)
// Kecepatan Kedip: 300ms (ON/OFF)
// =============================================================

// ============================================================
// KONFIGURASI PIN
// ============================================================
const int LED_PIN = 25;                      // Pin LED
const int RELAY_PIN = 2;                     // Pin Relay (buzzer/solenoid)

// ============================================================
// KONFIGURASI TIMING
// ============================================================
const unsigned long DOOR_DURATION = 10000;   // 10 detik
const unsigned long BLINK_INTERVAL = 300;    // Kedip 300ms
const unsigned long RELAY_PULSE = 500;       // Relay pulse 500ms (ON 250ms, OFF 250ms)
const unsigned long SMALL_DELAY = 50;        // Delay kecil prevent watchdog

// ============================================================
// SETUP
// ============================================================
void setup() {
  // Inisialisasi Serial Monitor (USB)
  Serial.begin(115200);
  delay(1000);
  
  Serial.println();
  Serial.println("╔═════════════════════════════════════════════════════╗");
  Serial.println("║ ESP32 DOOR CONTROL - USB SERIAL (BLINKING VERSION) ║");
  Serial.println("╚═════════════════════════════════════════════════════╝");

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
  Serial.println("   LED Kedip: 300ms ON/OFF");
  Serial.println("   Relay Bunyi: 500ms ON/OFF (pulsing)");
  Serial.println("   Durasi Pintu: 10 detik");
  Serial.println();
  Serial.println("📨 Pesan yang diterima:");
  Serial.println("   pintu=BUKA   → LED berkedip + RELAY pulsing (10s)");
  Serial.println("   pintu=TUTUP  → LED OFF, RELAY OFF (immediate)");
  Serial.println("   test=LED     → LED blink 1x");
  Serial.println("   test=RELAY   → RELAY pulse 2 detik");
  Serial.println("   status       → Get current status");
  Serial.println();
  Serial.println("─────────────────────────────────────────────────────");
  Serial.println();
}

// ============================================================
// LOOP UTAMA
// ============================================================
void loop() {
  // Cek apakah ada data dari Serial (USB)
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();  // Hapus whitespace
    
    if (message.length() == 0) return;  // Skip jika empty
    
    // Debug: tampilkan pesan yang diterima
    Serial.print("📡 Terima: ");
    Serial.println(message);

    // ========================================================
    // KONDISI 1: BUKA PINTU ⭐⭐⭐
    // ========================================================
    if (message == "pintu=BUKA") {
      Serial.println("🔓 BUKA PINTU!");
      Serial.println("💡 LED BERKEDIP (300ms) + 📣 RELAY PULSING (500ms)");
      Serial.println("⏱️  Durasi: 10 detik (auto-close)");
      Serial.println();
      
      // Timing variables
      unsigned long startTime = millis();
      unsigned long lastBlink = 0;
      unsigned long lastRelayPulse = 0;
      boolean ledState = LOW;
      boolean relayState = LOW;
      
      // Loop selama 10 detik
      while (millis() - startTime < DOOR_DURATION) {
        unsigned long elapsed = millis() - startTime;
        
        // ========================
        // LED BERKEDIP (300ms interval)
        // ========================
        if (elapsed - lastBlink >= BLINK_INTERVAL) {
          ledState = !ledState;  // Toggle LED
          digitalWrite(LED_PIN, ledState);
          lastBlink = elapsed;
          
          if (ledState == HIGH) {
            Serial.print(".");  // Visual feedback
          }
        }
        
        // ========================
        // RELAY PULSING (500ms interval - 250ms ON, 250ms OFF)
        // ========================
        if (elapsed - lastRelayPulse >= (RELAY_PULSE / 2)) {
          relayState = !relayState;
          digitalWrite(RELAY_PIN, relayState);
          lastRelayPulse = elapsed;
          
          if (relayState == HIGH) {
            Serial.print("🔊");  // Audio feedback
          }
        }
        
        // ========================
        // CHECK EARLY CLOSE (TUTUP command)
        // ========================
        if (Serial.available() > 0) {
          String earlyCmd = Serial.readStringUntil('\n');
          earlyCmd.trim();
          if (earlyCmd == "pintu=TUTUP") {
            Serial.println("\n");
            Serial.println("⚠️  TUTUP PINTU MANUAL!");
            digitalWrite(LED_PIN, LOW);
            digitalWrite(RELAY_PIN, LOW);
            Serial.println("✅ SELESAI (TUTUP MANUAL)");
            return;  // Keluar dari loop
          }
        }
        
        delay(SMALL_DELAY);  // Prevent watchdog timeout
      }
      
      // ===== SETELAH 10 DETIK =====
      Serial.println("\n");
      digitalWrite(LED_PIN, LOW);
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("💡 LED OFF");
      Serial.println("📣 RELAY OFF");
      Serial.println("✅ SELESAI (Auto-close 10 detik)");
      Serial.println();
    }

    // ========================================================
    // KONDISI 2: TUTUP PINTU (IMMEDIATE)
    // ========================================================
    else if (message == "pintu=TUTUP") {
      Serial.println("🔒 TUTUP PINTU!");
      digitalWrite(LED_PIN, LOW);
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("💡 LED OFF");
      Serial.println("📣 RELAY OFF");
      Serial.println("✅ SELESAI");
      Serial.println();
    }

    // ========================================================
    // KONDISI 3: TEST LED
    // ========================================================
    else if (message == "test=LED") {
      Serial.println("💡 TEST LED - Blink 3x");
      for (int i = 0; i < 3; i++) {
        digitalWrite(LED_PIN, HIGH);
        Serial.print("✓");
        delay(500);
        digitalWrite(LED_PIN, LOW);
        delay(300);
      }
      Serial.println();
      Serial.println("✅ LED test selesai");
      Serial.println();
    }

    // ========================================================
    // KONDISI 4: TEST RELAY
    // ========================================================
    else if (message == "test=RELAY") {
      Serial.println("⚡ TEST RELAY - Pulse 2 detik");
      unsigned long testStart = millis();
      unsigned long testDuration = 2000;
      unsigned long lastPulse = 0;
      boolean testState = LOW;
      
      while (millis() - testStart < testDuration) {
        if (millis() - testStart - lastPulse >= 500) {
          testState = !testState;
          digitalWrite(RELAY_PIN, testState);
          Serial.print("🔊");
          lastPulse = millis() - testStart;
        }
        delay(50);
      }
      
      digitalWrite(RELAY_PIN, LOW);
      Serial.println();
      Serial.println("✅ RELAY test selesai");
      Serial.println();
    }

    // ========================================================
    // KONDISI 5: STATUS
    // ========================================================
    else if (message == "status") {
      int ledStatus = digitalRead(LED_PIN);
      int relayStatus = digitalRead(RELAY_PIN);
      Serial.println("📊 STATUS:");
      Serial.print("   LED: ");
      Serial.println(ledStatus == HIGH ? "ON 💡" : "OFF ⚫");
      Serial.print("   RELAY: ");
      Serial.println(relayStatus == HIGH ? "ON 🔊" : "OFF 🔇");
      Serial.println();
    }

    // ========================================================
    // PESAN TIDAK DIKENAL
    // ========================================================
    else {
      Serial.print("⚠️  Pesan tidak dikenal: ");
      Serial.println(message);
      Serial.println("📨 Command yang valid:");
      Serial.println("   - pintu=BUKA");
      Serial.println("   - pintu=TUTUP");
      Serial.println("   - test=LED");
      Serial.println("   - test=RELAY");
      Serial.println("   - status");
      Serial.println();
    }
  }
}

// ============================================================
// NOTES & CONFIGURATION
// ============================================================
/*
TIMING CONFIGURATION:

LED Berkedip:
  - Interval: 300ms (ON 150ms, OFF 150ms)
  - Ubah BLINK_INTERVAL untuk speed berbeda

RELAY Pulsing:
  - Interval: 500ms (ON 250ms, OFF 250ms)
  - Ubah RELAY_PULSE untuk pattern berbeda

Door Duration:
  - Default: 10 detik
  - Ubah DOOR_DURATION untuk durasi berbeda

Contoh durasi lain:
  - DOOR_DURATION = 5000    (5 detik)
  - DOOR_DURATION = 15000   (15 detik)
  - DOOR_DURATION = 20000   (20 detik)

UNTUK RGB LED (OPTIONAL):
Jika ingin warna warni, gunakan 3 pin RGB:
  const int LED_R = 25;  // Red
  const int LED_G = 26;  // Green
  const int LED_B = 27;  // Blue

Kemudian ganti:
  digitalWrite(LED_PIN, ledState);
dengan:
  if (ledState == HIGH) {
    digitalWrite(LED_R, HIGH);  // Merah
  } else {
    digitalWrite(LED_R, LOW);
  }
*/
