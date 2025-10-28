// =============================================================
// ESP32 DEBUG & TESTING SCRIPT
// =============================================================
// Script untuk troubleshooting dan testing ESP32
// Gunakan ini jika ada masalah dengan main script
//
// Features:
//   - Test WiFi connection
//   - Test MQTT connection
//   - Test LED blink
//   - Test Relay toggle
//   - Monitor sensor input
//   - Serial debugging
// =============================================================

#include <WiFi.h>
#include <PubSubClient.h>

// ============================================================
// KONFIGURASI
// ============================================================
const char* ssid = "YOUR_SSID";
const char* password = "YOUR_PASSWORD";
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "fc/pintu";
const char* mqtt_id = "esp32_debug_01";

// Pin configuration
const int LED_PIN = 25;
const int RELAY_PIN = 2;

// Global variables
WiFiClient espClient;
PubSubClient client(espClient);
unsigned long testStartTime = 0;
int testMode = 0; // 0=idle, 1=wifi_test, 2=mqtt_test, 3=led_test, 4=relay_test

// ============================================================
// SERIAL MENU
// ============================================================
void printMenu() {
  Serial.println();
  Serial.println("╔═══════════════════════════════════════════╗");
  Serial.println("║     ESP32 DEBUG & TESTING MENU            ║");
  Serial.println("╚═══════════════════════════════════════════╝");
  Serial.println();
  Serial.println("Pilih test (ketik nomor + Enter):");
  Serial.println();
  Serial.println("  1 = Test WiFi Connection");
  Serial.println("  2 = Test MQTT Connection");
  Serial.println("  3 = Test LED (blink 5x)");
  Serial.println("  4 = Test Relay (toggle 3x)");
  Serial.println("  5 = Test Full System (WiFi + MQTT + LED + Relay)");
  Serial.println("  6 = Monitor Status (auto-refresh every 5 detik)");
  Serial.println("  0 = Show this menu");
  Serial.println();
  Serial.print("Input: ");
}

// ============================================================
// WIFI TEST
// ============================================================
void testWiFi() {
  Serial.println();
  Serial.println("🔄 [TEST 1] WIFI CONNECTION TEST");
  Serial.println("════════════════════════════════════════════");
  
  Serial.print("Menghubungkan ke: ");
  Serial.println(ssid);
  
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }
  
  Serial.println();
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("✅ WIFI BERHASIL TERHUBUNG!");
    Serial.print("   IP Address: ");
    Serial.println(WiFi.localIP());
    Serial.print("   RSSI (Signal Strength): ");
    Serial.println(WiFi.RSSI());
    Serial.print("   Gateway: ");
    Serial.println(WiFi.gatewayIP());
    Serial.print("   Subnet: ");
    Serial.println(WiFi.subnetMask());
  } else {
    Serial.println("❌ GAGAL TERHUBUNG KE WIFI!");
    Serial.println("   Cek: SSID, Password, dan jangkauan WiFi");
  }
  
  Serial.println("════════════════════════════════════════════");
  printMenu();
}

// ============================================================
// MQTT TEST
// ============================================================
void testMQTT() {
  Serial.println();
  Serial.println("🔄 [TEST 2] MQTT CONNECTION TEST");
  Serial.println("════════════════════════════════════════════");
  
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("❌ WiFi belum terhubung! Lakukan Test 1 dulu.");
    Serial.println("════════════════════════════════════════════");
    printMenu();
    return;
  }
  
  Serial.print("Menghubungkan ke: ");
  Serial.print(mqtt_server);
  Serial.print(":");
  Serial.println(mqtt_port);
  
  client.setServer(mqtt_server, mqtt_port);
  
  if (client.connect(mqtt_id)) {
    Serial.println("✅ MQTT BERHASIL TERHUBUNG!");
    Serial.print("   Broker: ");
    Serial.println(mqtt_server);
    Serial.print("   ID: ");
    Serial.println(mqtt_id);
    
    // Subscribe to topic
    Serial.print("   Subscribe to: ");
    Serial.println(mqtt_topic);
    client.subscribe(mqtt_topic);
    
    // Publish status
    client.publish(mqtt_topic, "DEBUG=TEST_HELLO");
    Serial.println("   Publish: DEBUG=TEST_HELLO");
    
    // Test receive
    Serial.println();
    Serial.println("Tunggu 5 detik untuk terima pesan...");
    for (int i = 0; i < 5; i++) {
      client.loop();
      delay(1000);
      Serial.print(".");
    }
    Serial.println();
    
  } else {
    Serial.print("❌ MQTT GAGAL TERHUBUNG! Error code: ");
    Serial.println(client.state());
    Serial.println("   Cek: Broker URL, Port, dan koneksi internet");
  }
  
  Serial.println("════════════════════════════════════════════");
  printMenu();
}

// ============================================================
// LED TEST
// ============================================================
void testLED() {
  Serial.println();
  Serial.println("🔄 [TEST 3] LED TEST (GPIO 25)");
  Serial.println("════════════════════════════════════════════");
  Serial.println("LED akan blink 5 kali...");
  
  for (int i = 1; i <= 5; i++) {
    Serial.print("Blink #");
    Serial.print(i);
    Serial.print(" - ");
    
    // ON
    digitalWrite(LED_PIN, HIGH);
    Serial.print("ON ");
    delay(500);
    
    // OFF
    digitalWrite(LED_PIN, LOW);
    Serial.println("OFF");
    delay(500);
  }
  
  Serial.println();
  Serial.println("✅ LED TEST SELESAI!");
  Serial.println("   Amati LED untuk pastikan bekerja normal");
  Serial.println("════════════════════════════════════════════");
  printMenu();
}

// ============================================================
// RELAY TEST
// ============================================================
void testRelay() {
  Serial.println();
  Serial.println("🔄 [TEST 4] RELAY TEST (GPIO 2)");
  Serial.println("════════════════════════════════════════════");
  Serial.println("Relay akan toggle 3 kali (ON 2 detik, OFF 1 detik)...");
  
  for (int i = 1; i <= 3; i++) {
    Serial.print("Toggle #");
    Serial.print(i);
    Serial.print(" - ");
    
    // ON
    digitalWrite(RELAY_PIN, HIGH);
    Serial.print("ON (2 detik) ");
    delay(2000);
    
    // OFF
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("OFF (1 detik)");
    delay(1000);
  }
  
  Serial.println();
  Serial.println("✅ RELAY TEST SELESAI!");
  Serial.println("   Dengarkan buzzer/solenoid untuk pastikan bekerja");
  Serial.println("════════════════════════════════════════════");
  printMenu();
}

// ============================================================
// FULL SYSTEM TEST
// ============================================================
void testFullSystem() {
  Serial.println();
  Serial.println("🔄 [TEST 5] FULL SYSTEM TEST");
  Serial.println("════════════════════════════════════════════");
  
  // Step 1: WiFi
  Serial.println("[Step 1/4] Testing WiFi...");
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  
  int wifiAttempts = 0;
  while (WiFi.status() != WL_CONNECTED && wifiAttempts < 15) {
    delay(500);
    Serial.print(".");
    wifiAttempts++;
  }
  
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println(" ✅");
    Serial.print("   IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println(" ❌ WiFi failed!");
    Serial.println("════════════════════════════════════════════");
    printMenu();
    return;
  }
  
  // Step 2: MQTT
  Serial.println("[Step 2/4] Testing MQTT...");
  client.setServer(mqtt_server, mqtt_port);
  
  if (client.connect(mqtt_id)) {
    Serial.println(" ✅");
    client.subscribe(mqtt_topic);
  } else {
    Serial.println(" ❌ MQTT failed!");
    Serial.println("════════════════════════════════════════════");
    printMenu();
    return;
  }
  
  // Step 3: LED
  Serial.println("[Step 3/4] Testing LED...");
  digitalWrite(LED_PIN, HIGH);
  delay(1000);
  digitalWrite(LED_PIN, LOW);
  delay(500);
  Serial.println(" ✅");
  
  // Step 4: Relay
  Serial.println("[Step 4/4] Testing Relay...");
  digitalWrite(RELAY_PIN, HIGH);
  delay(2000);
  digitalWrite(RELAY_PIN, LOW);
  Serial.println(" ✅");
  
  Serial.println();
  Serial.println("════════════════════════════════════════════");
  Serial.println("✅✅✅ SEMUA TEST BERHASIL! ✅✅✅");
  Serial.println("════════════════════════════════════════════");
  printMenu();
}

// ============================================================
// MONITOR STATUS
// ============================================================
void monitorStatus() {
  Serial.println();
  Serial.println("🔄 [TEST 6] MONITOR STATUS (tekan Ctrl+C untuk stop)");
  Serial.println("════════════════════════════════════════════");
  
  unsigned long lastPrint = 0;
  
  while (true) {
    // Print setiap 5 detik
    if (millis() - lastPrint > 5000) {
      lastPrint = millis();
      
      Serial.println();
      Serial.println("─────────────────────────────────────────");
      Serial.print("⏰ Waktu: ");
      Serial.print(millis() / 1000);
      Serial.println(" detik");
      
      Serial.print("🌐 WiFi: ");
      if (WiFi.status() == WL_CONNECTED) {
        Serial.print("✅ TERHUBUNG (IP: ");
        Serial.print(WiFi.localIP());
        Serial.print(", RSSI: ");
        Serial.print(WiFi.RSSI());
        Serial.println(")");
      } else {
        Serial.println("❌ TERPUTUS");
      }
      
      Serial.print("📡 MQTT: ");
      Serial.println(client.connected() ? "✅ TERHUBUNG" : "❌ TERPUTUS");
      
      Serial.print("💡 LED Status: ");
      Serial.println(digitalRead(LED_PIN) ? "🔴 ON" : "⚫ OFF");
      
      Serial.print("📣 Relay Status: ");
      Serial.println(digitalRead(RELAY_PIN) ? "🔴 ON" : "⚫ OFF");
      
      Serial.println("─────────────────────────────────────────");
    }
    
    // Check serial input
    if (Serial.available()) {
      char input = Serial.read();
      if (input == '\n' || input == '\r') {
        break;
      }
    }
    
    delay(100);
  }
  
  printMenu();
}

// ============================================================
// MQTT CALLBACK
// ============================================================
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }
  
  Serial.println();
  Serial.print("📡 MQTT Message received: ");
  Serial.println(message);
  
  if (message == "pintu=BUKA") {
    digitalWrite(LED_PIN, HIGH);
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("   → LED ON, Relay ON");
  } else if (message == "pintu=TUTUP") {
    digitalWrite(LED_PIN, LOW);
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("   → LED OFF, Relay OFF");
  }
  
  Serial.print("Input: ");
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  Serial.begin(115200);
  delay(1000);
  
  // Setup pins
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(LED_PIN, LOW);
  digitalWrite(RELAY_PIN, LOW);
  
  // Setup MQTT callback
  client.setCallback(mqtt_callback);
  
  // Print header
  Serial.println();
  Serial.println("╔═══════════════════════════════════════════╗");
  Serial.println("║   ESP32 DEBUG & TESTING SUITE             ║");
  Serial.println("╚═══════════════════════════════════════════╝");
  Serial.println();
  Serial.println("Pins configured:");
  Serial.print("   LED:   GPIO ");
  Serial.println(LED_PIN);
  Serial.print("   Relay: GPIO ");
  Serial.println(RELAY_PIN);
  
  printMenu();
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  if (Serial.available()) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    
    if (input == "1") {
      testWiFi();
    }
    else if (input == "2") {
      testMQTT();
    }
    else if (input == "3") {
      testLED();
    }
    else if (input == "4") {
      testRelay();
    }
    else if (input == "5") {
      testFullSystem();
    }
    else if (input == "6") {
      monitorStatus();
    }
    else if (input == "0") {
      printMenu();
    }
    else {
      Serial.println("❌ Input tidak dikenali! Pilih 0-6");
      printMenu();
    }
  }
  
  // Keep MQTT connection alive
  if (WiFi.status() == WL_CONNECTED && client.connected()) {
    client.loop();
  }
  
  delay(100);
}

// =============================================================
// CARA PAKAI:
// =============================================================
// 1. Upload script ini ke ESP32
// 2. Buka Serial Monitor (115200 baud)
// 3. Ikuti menu yang tersedia
// 4. Pilih test yang ingin dijalankan
// 5. Lihat output dan debugging messages
// =============================================================
