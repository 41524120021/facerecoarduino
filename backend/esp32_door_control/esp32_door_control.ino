/*
  ==============================================================
  ESP32 MQTT Door Control
  --------------------------------------------------------------
  Fungsi:
    - Terhubung ke broker MQTT publik HiveMQ
    - Subscribe ke topik: "teguhdayanto/esp32/pintu"
    - Saat menerima pesan:
        "pintu=BUKA"  → LED pin 2 ON (pintu terbuka)
        "pintu=TUTUP" → LED pin 2 OFF (pintu tertutup)
  ==============================================================
*/

#include <WiFi.h>
#include <PubSubClient.h>

// --------------------------------------------------------------
// KONFIGURASI WIFI & MQTT
// --------------------------------------------------------------
const char* ssid = "Diklat-BPSDMI-PIDI";
const char* password = "1234512345";

const char* mqtt_server = "broker.hivemq.com"; // Broker publik HiveMQ
const int mqtt_port = 1883;

WiFiClient espClient;
PubSubClient client(espClient);

const int ledPin = 2; // LED terhubung ke pin 2

// --------------------------------------------------------------
// CALLBACK — Fungsi yang dipanggil saat pesan MQTT diterima
// --------------------------------------------------------------
void callback(char* topic, byte* payload, unsigned int length) {
  String message;
  for (int i = 0; i < length; i++) {
    message += (char)payload[i];
  }

  Serial.println("=================================");
  Serial.print("📩 Pesan diterima dari topik: ");
  Serial.println(topic);
  Serial.print("🗨️  Isi pesan: ");
  Serial.println(message);

  // ------------------------------------------------------------
  // Analisis pesan dan kontrol LED
  // ------------------------------------------------------------
  if (message == "pintu=BUKA") {
    digitalWrite(ledPin, HIGH);
    Serial.println("🚪 LED ON — Pintu Terbuka");
  } else if (message == "pintu=TUTUP") {
    digitalWrite(ledPin, LOW);
    Serial.println("🔒 LED OFF — Pintu Tertutup");
  }
  Serial.println("=================================");
}

// --------------------------------------------------------------
// RECONNECT — Coba sambung ulang ke broker jika terputus
// --------------------------------------------------------------
void reconnect() {
  while (!client.connected()) {
    Serial.print("🔄 Menghubungkan ke broker MQTT...");
    if (client.connect("ESP32Client")) {
      Serial.println("✅ Terhubung ke HiveMQ!");
      client.subscribe("PascalisB/esp32/pintu");
      Serial.println("📡 Berlangganan topik: PascalisB/esp32/pintu");
    } else {
      Serial.print("❌ Gagal, rc=");
      Serial.print(client.state());
      Serial.println(" coba lagi dalam 5 detik...");
      delay(5000);
    }
  }
}

// --------------------------------------------------------------
// SETUP — Koneksi WiFi & MQTT
// --------------------------------------------------------------
void setup() {
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  Serial.begin(115200);
  Serial.println("🚀 Memulai ESP32 MQTT Door Control...");

  // Koneksi ke WiFi
  Serial.print("🔌 Menghubungkan ke WiFi ");
  Serial.print(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi terhubung!");
  Serial.print("📶 IP Address: ");
  Serial.println(WiFi.localIP());

  // Koneksi ke broker MQTT
  client.setServer(mqtt_server, mqtt_port);
  client.setCallback(callback);
}

// --------------------------------------------------------------
// LOOP — Jalankan koneksi MQTT terus menerus
// --------------------------------------------------------------
void loop() {
  if (!client.connected()) {
    reconnect();
  }
  client.loop();
}
