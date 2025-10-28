// =============================================================
// ESP32 DOOR CONTROL SYSTEM
// =============================================================
// Fitur:
//   - Terima pesan MQTT dari Flask backend
//   - Kontrol LED (pin 25) dan Relay (pin 2)
//   - Ketika pesan "pintu=BUKA" → LED ON, Relay ON (buzzer bunyi)
//   - Ketika pesan "pintu=TUTUP" → LED OFF, Relay OFF (buzzer diam)
// 
// Koneksi Hardware:
//   - LED       → GPIO 25 (LED biru/merah)
//   - Relay     → GPIO 2  (Relay untuk buzzer/solenoid)
//   - WiFi      → onboard (built-in)
// 
// Broker MQTT: broker.hivemq.com
// Topik MQTT : fc/pintu
// =============================================================

#include <WiFi.h>
#include <PubSubClient.h>

// ============================================================
// KONFIGURASI WIFI
// ============================================================
const char* ssid = "YOUR_SSID";              // Ganti dengan SSID WiFi Anda
const char* password = "YOUR_PASSWORD";      // Ganti dengan password WiFi Anda

// ============================================================
// KONFIGURASI MQTT
// ============================================================
const char* mqtt_server = "broker.hivemq.com";
const int mqtt_port = 1883;
const char* mqtt_topic = "fc/pintu";         // Topik MQTT (harus sama dengan app.py)
const char* mqtt_id = "esp32_door_01";       // ID unik ESP32

// ============================================================
// KONFIGURASI PIN
// ============================================================
const int LED_PIN = 25;                      // Pin LED
const int RELAY_PIN = 2;                     // Pin Relay (buzzer/solenoid)

// ============================================================
// DEKLARASI OBJEK
// ============================================================
WiFiClient espClient;
PubSubClient client(espClient);

// ============================================================
// FUNGSI: CONNECT WIFI
// ============================================================
void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("🔄 Menghubungkan ke WIFI: ");
  Serial.println(ssid);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 20) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.println("✅ WIFI Terhubung!");
    Serial.print("📍 IP Address: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println();
    Serial.println("❌ Gagal terhubung ke WIFI. Cek SSID dan Password.");
  }
}

// ============================================================
// FUNGSI: CALLBACK MQTT (TERIMA PESAN)
// ============================================================
void mqtt_callback(char* topic, byte* payload, unsigned int length) {
  // Konversi payload ke string
  String message = "";
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.print("📡 MQTT Terima: ");
  Serial.print(topic);
  Serial.print(" → ");
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
    delay(10000);
    
    // Matikan LED dan Relay (automatic)
    digitalWrite(LED_PIN, LOW);
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("💡 LED OFF");
    Serial.println("📣 RELAY OFF (Buzzer diam)");
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
}

// ============================================================
// FUNGSI: RECONNECT MQTT
// ============================================================
void reconnect() {
  int attempts = 0;
  
  while (!client.connected() && attempts < 5) {
    Serial.print("🔄 Mencoba connect ke MQTT broker...");
    
    if (client.connect(mqtt_id)) {
      Serial.println(" ✅ Connected!");
      
      // Subscribe ke topik MQTT
      client.subscribe(mqtt_topic);
      Serial.print("✅ Subscribe ke topik: ");
      Serial.println(mqtt_topic);
      
      // Publish status online
      client.publish(mqtt_topic, "status=ONLINE");
      Serial.println("📡 Publish: status=ONLINE");
    } else {
      Serial.print(" ❌ Failed (rc=");
      Serial.print(client.state());
      Serial.println("), coba lagi dalam 5 detik...");
      delay(5000);
      attempts++;
    }
  }
}

// ============================================================
// SETUP
// ============================================================
void setup() {
  // Inisialisasi Serial Monitor
  Serial.begin(115200);
  delay(1000);
  
  Serial.println();
  Serial.println("╔═══════════════════════════════════════════════════╗");
  Serial.println("║   ESP32 DOOR CONTROL SYSTEM - Face Recognition   ║");
  Serial.println("╚═══════════════════════════════════════════════════╝");

  // Setup PIN
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // Matikan semua output di awal
  digitalWrite(LED_PIN, LOW);
  digitalWrite(RELAY_PIN, LOW);
  
  Serial.println("✅ PIN Setup: LED (GPIO 25) dan RELAY (GPIO 2)");

  // Setup WiFi
  setup_wifi();

  // Setup MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(mqtt_callback);

  Serial.println();
  Serial.println("📊 Konfigurasi:");
  Serial.print("   Broker: ");
  Serial.println(mqtt_server);
  Serial.print("   Topik: ");
  Serial.println(mqtt_topic);
  Serial.print("   ID MQTT: ");
  Serial.println(mqtt_id);
  Serial.println();
}

// ============================================================
// LOOP
// ============================================================
void loop() {
  // ========================================================
  // RECONNECT WIFI JIKA TERPUTUS
  // ========================================================
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("⚠️  WIFI terputus, mencoba reconnect...");
    setup_wifi();
    delay(5000);
    return;
  }

  // ========================================================
  // RECONNECT MQTT JIKA TERPUTUS
  // ========================================================
  if (!client.connected()) {
    reconnect();
  }

  // ========================================================
  // PROSES PESAN MQTT
  // ========================================================
  client.loop();

  // ========================================================
  // STATUS SETIAP 30 DETIK (DEBUG)
  // ========================================================
  static unsigned long lastStatusTime = 0;
  if (millis() - lastStatusTime > 30000) {
    lastStatusTime = millis();
    
    Serial.println();
    Serial.println("═══════════════════════════════════════");
    Serial.print("⏰ Status LED: ");
    Serial.println(digitalRead(LED_PIN) ? "ON 💡" : "OFF");
    Serial.print("⏰ Status RELAY: ");
    Serial.println(digitalRead(RELAY_PIN) ? "ON 📣" : "OFF");
    Serial.print("📡 MQTT Connected: ");
    Serial.println(client.connected() ? "✅ Yes" : "❌ No");
    Serial.print("🌐 WIFI Signal: ");
    Serial.println(WiFi.RSSI());
    Serial.println("═══════════════════════════════════════");
  }

  delay(100);
}

// =============================================================
// CATATAN INSTALASI:
// =============================================================
// 1. Install Arduino IDE (https://www.arduino.cc/en/software)
// 2. Add Board Manager ESP32:
//    Tools → Board Manager → Search "esp32" → Install by Espressif
// 3. Install Library PubSubClient:
//    Sketch → Include Library → Manage Libraries
//    Search "PubSubClient" → Install by Nick O'Leary
// 4. Ganti SSID dan PASSWORD WiFi
// 5. Hubungkan ESP32 via USB
// 6. Select: Tools → Board → DOIT ESP32 DEVKIT V1
// 7. Select: Tools → Port → COMx (cek di Device Manager)
// 8. Upload sketch
// 9. Buka Serial Monitor (Tools → Serial Monitor) untuk debug
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
// 5V         →  VCC (+ Relay)
// GND        →  GND (- Relay)
//
// Relay OUT  →  Buzzer/Solenoid Lock
// =============================================================
// TEST DENGAN MQTT:
// =============================================================
// Buka MQTT client (mosquitto/MQTT.fx):
// Publish ke "fc/pintu" dengan payload:
//   - pintu=BUKA       → LED ON, Relay ON (10 detik)
//   - pintu=TUTUP      → LED OFF, Relay OFF
//   - test=LED         → Test LED (blink 1x)
//   - test=RELAY       → Test Relay (on 2 detik)
// =============================================================
