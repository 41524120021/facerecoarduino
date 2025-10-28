// =============================================================
// ESP32 DOOR CONTROL - RGB LED VERSION
// LED WARNA WARNI BERKEDIP + RELAY TERUS BUNYI
// =============================================================
// Fitur:
//   - RGB LED (merah, hijau, biru, warna campuran)
//   - Warna berganti setiap kedip (rainbow effect)
//   - Relay terus pulsing (bunyi) selama pintu buka
//   - Durasi: 10 detik
// 
// Pin Configuration:
//   - LED Red   → GPIO 25
//   - LED Green → GPIO 26
//   - LED Blue  → GPIO 27
//   - Relay     → GPIO 2
//   - USB       → Serial (115200 baud)
// 
// Kontrol:
//   - pintu=BUKA   → RGB LED berubah warna + RELAY pulsing (10s)
//   - pintu=TUTUP  → Semua OFF
//   - test=LED     → Test RGB colors
// =============================================================

// ============================================================
// KONFIGURASI PIN RGB
// ============================================================
const int LED_R = 25;                        // Red
const int LED_G = 26;                        // Green
const int LED_B = 27;                        // Blue
const int RELAY_PIN = 2;                     // Relay

// ============================================================
// TIMING
// ============================================================
const unsigned long DOOR_DURATION = 10000;   // 10 detik
const unsigned long COLOR_CHANGE = 500;      // Ganti warna setiap 500ms
const unsigned long RELAY_PULSE = 500;       // Relay pulse 500ms
const unsigned long SMALL_DELAY = 50;        // Prevent watchdog

// ============================================================
// WARNA RGB (dapat dikustomisasi)
// ============================================================
struct RGB {
  int r, g, b;
};

// Array warna rainbow
const RGB colors[] = {
  {255, 0, 0},      // Merah
  {255, 127, 0},    // Orange (red + green)
  {255, 255, 0},    // Kuning (red + green)
  {0, 255, 0},      // Hijau
  {0, 255, 255},    // Cyan (green + blue)
  {0, 0, 255},      // Biru
  {255, 0, 255},    // Magenta (red + blue)
};
const int NUM_COLORS = 7;

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  Serial.println();
  Serial.println("╔═════════════════════════════════════════════════════╗");
  Serial.println("║ ESP32 DOOR CONTROL - RGB LED (RAINBOW BLINKING)   ║");
  Serial.println("╚═════════════════════════════════════════════════════╝");

  // Setup RGB pins
  pinMode(LED_R, OUTPUT);
  pinMode(LED_G, OUTPUT);
  pinMode(LED_B, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // All OFF di awal
  turnOffAllLED();
  digitalWrite(RELAY_PIN, LOW);
  
  Serial.println("✅ PIN Setup: RGB LED (GPIO 25,26,27) + RELAY (GPIO 2)");
  Serial.println();
  Serial.println("📊 Konfigurasi:");
  Serial.println("   LED: RGB dengan 7 warna (Rainbow)");
  Serial.println("   Perubahan warna: 500ms");
  Serial.println("   Relay Bunyi: 500ms pulsing");
  Serial.println("   Durasi Pintu: 10 detik");
  Serial.println();
  Serial.println("📨 Commands:");
  Serial.println("   pintu=BUKA    → RGB berubah warna + RELAY pulsing");
  Serial.println("   pintu=TUTUP   → Semua OFF");
  Serial.println("   test=LED      → Test semua warna");
  Serial.println("   status        → Status current");
  Serial.println();
  Serial.println("─────────────────────────────────────────────────────");
  Serial.println();
}

// ============================================================
// FUNGSI: SET WARNA RGB (PWM untuk brightness)
// ============================================================
void setRGB(int r, int g, int b) {
  // Gunakan PWM untuk brightness control (0-255)
  analogWrite(LED_R, r);
  analogWrite(LED_G, g);
  analogWrite(LED_B, b);
}

// ============================================================
// FUNGSI: MATIKAN SEMUA LED
// ============================================================
void turnOffAllLED() {
  setRGB(0, 0, 0);
}

// ============================================================
// FUNGSI: GET COLOR BY INDEX
// ============================================================
RGB getColor(int index) {
  return colors[index % NUM_COLORS];
}

// ============================================================
// LOOP UTAMA
// ============================================================
void loop() {
  if (Serial.available() > 0) {
    String message = Serial.readStringUntil('\n');
    message.trim();
    
    if (message.length() == 0) return;
    
    Serial.print("📡 Terima: ");
    Serial.println(message);

    // ========================================================
    // BUKA PINTU - RGB RAINBOW + RELAY PULSING ⭐
    // ========================================================
    if (message == "pintu=BUKA") {
      Serial.println("🔓 BUKA PINTU!");
      Serial.println("🌈 RGB LED berubah warna + 📣 RELAY pulsing (10 detik)");
      Serial.println();
      
      unsigned long startTime = millis();
      unsigned long lastColorChange = 0;
      unsigned long lastRelayPulse = 0;
      int colorIndex = 0;
      boolean relayState = LOW;
      
      // Loop 10 detik
      while (millis() - startTime < DOOR_DURATION) {
        unsigned long elapsed = millis() - startTime;
        
        // ========================
        // RGB BERUBAH WARNA (500ms)
        // ========================
        if (elapsed - lastColorChange >= COLOR_CHANGE) {
          RGB currentColor = getColor(colorIndex);
          setRGB(currentColor.r, currentColor.g, currentColor.b);
          colorIndex++;
          lastColorChange = elapsed;
          
          Serial.print("🌈");  // Visual feedback
        }
        
        // ========================
        // RELAY PULSING (500ms - ON/OFF)
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
        // CHECK EARLY CLOSE
        // ========================
        if (Serial.available() > 0) {
          String earlyCmd = Serial.readStringUntil('\n');
          earlyCmd.trim();
          if (earlyCmd == "pintu=TUTUP") {
            Serial.println("\n");
            Serial.println("⚠️  TUTUP PINTU MANUAL!");
            turnOffAllLED();
            digitalWrite(RELAY_PIN, LOW);
            Serial.println("✅ SELESAI (TUTUP MANUAL)");
            return;
          }
        }
        
        delay(SMALL_DELAY);
      }
      
      // ===== AFTER 10 SECONDS =====
      Serial.println("\n");
      turnOffAllLED();
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("🌈 RGB LED OFF");
      Serial.println("📣 RELAY OFF");
      Serial.println("✅ SELESAI (Auto-close 10 detik)");
      Serial.println();
    }

    // ========================================================
    // TUTUP PINTU
    // ========================================================
    else if (message == "pintu=TUTUP") {
      Serial.println("🔒 TUTUP PINTU!");
      turnOffAllLED();
      digitalWrite(RELAY_PIN, LOW);
      Serial.println("🌈 RGB LED OFF");
      Serial.println("📣 RELAY OFF");
      Serial.println("✅ SELESAI");
      Serial.println();
    }

    // ========================================================
    // TEST LED - TAMPILKAN SEMUA WARNA
    // ========================================================
    else if (message == "test=LED") {
      Serial.println("🌈 TEST RGB - Tampilkan semua warna (2 detik each)");
      Serial.println();
      
      for (int i = 0; i < NUM_COLORS; i++) {
        RGB color = getColor(i);
        setRGB(color.r, color.g, color.b);
        
        // Print nama warna
        switch (i) {
          case 0: Serial.println("  🔴 Merah"); break;
          case 1: Serial.println("  🟠 Orange"); break;
          case 2: Serial.println("  🟡 Kuning"); break;
          case 3: Serial.println("  🟢 Hijau"); break;
          case 4: Serial.println("  🔵 Cyan"); break;
          case 5: Serial.println("  🔵 Biru"); break;
          case 6: Serial.println("  🟣 Magenta"); break;
        }
        
        delay(2000);  // 2 detik per warna
      }
      
      turnOffAllLED();
      Serial.println();
      Serial.println("✅ RGB test selesai");
      Serial.println();
    }

    // ========================================================
    // TEST RELAY
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
    // STATUS
    // ========================================================
    else if (message == "status") {
      Serial.println("📊 STATUS:");
      Serial.print("   LED: ");
      if (digitalRead(LED_R) || digitalRead(LED_G) || digitalRead(LED_B)) {
        Serial.println("ON 🌈");
      } else {
        Serial.println("OFF ⚫");
      }
      Serial.print("   RELAY: ");
      Serial.println(digitalRead(RELAY_PIN) == HIGH ? "ON 🔊" : "OFF 🔇");
      Serial.println();
    }

    // ========================================================
    // UNKNOWN COMMAND
    // ========================================================
    else {
      Serial.print("⚠️  Unknown command: ");
      Serial.println(message);
      Serial.println("📨 Valid commands:");
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
// CUSTOMIZATION TIPS
// ============================================================
/*
WARNA RGB:
  
Merah:       setRGB(255, 0, 0)
Hijau:       setRGB(0, 255, 0)
Biru:        setRGB(0, 0, 255)
Kuning:      setRGB(255, 255, 0)
Cyan:        setRGB(0, 255, 255)
Magenta:     setRGB(255, 0, 255)
Putih:       setRGB(255, 255, 255)
Orange:      setRGB(255, 165, 0)
Pink:        setRGB(255, 192, 203)

MENAMBAH/MENGUBAH WARNA:
Ubah array colors[] di atas dengan kombinasi baru:

const RGB colors[] = {
  {255, 0, 0},      // Red
  {0, 255, 0},      // Green
  {0, 0, 255},      // Blue
  // Tambah lebih banyak...
};

KECEPATAN PERUBAHAN WARNA:
Ubah COLOR_CHANGE:
  - 300ms: Cepat
  - 500ms: Medium (default)
  - 1000ms: Lambat

KECEPATAN RELAY PULSING:
Ubah RELAY_PULSE:
  - 200ms: Cepat (bunyi cepat)
  - 500ms: Medium (default)
  - 1000ms: Lambat
*/
