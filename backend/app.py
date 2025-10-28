# =============================================================
# APP.PY — Sistem Face Recognition + Kontrol Pintu via MQTT
# -------------------------------------------------------------
# Fungsi:
#  - Deteksi wajah menggunakan camera (OpenCV + face_recognition)
#  - Jika wajah dikenal → tombol "Buka Pintu" aktif di web
#  - Saat ditekan → kirim pesan MQTT ke ESP32:
#       pintu=BUKA  → LED ESP32 ON
#       tunggu 10 detik
#       pintu=TUTUP → LED ESP32 OFF
# Broker MQTT: broker.hivemq.com (public)
# Topik MQTT : teguhdayanto/esp32/pintu
# =============================================================

from flask import Flask, render_template, Response, request
import cv2
import face_recognition
import os
import requests
import time
import json
import paho.mqtt.client as mqtt

# -------------------------------------------------------------
# KONFIGURASI UTAMA
# -------------------------------------------------------------
app = Flask(__name__)
camera = cv2.VideoCapture(0)

DATASET_PATH = "../dataset"        # Folder dataset wajah
MQTT_BROKER = "broker.hivemq.com"  # Broker MQTT publik
MQTT_PORT = 1883
MQTT_TOPIC = "fc/galih"

# -------------------------------------------------------------
# MUAT SEMUA DATASET WAJAH YANG DIKENAL
# -------------------------------------------------------------
known_face_encodings = []
known_face_names = []

for person_name in os.listdir(DATASET_PATH):
    folder = os.path.join(DATASET_PATH, person_name)
    if not os.path.isdir(folder):
        continue
    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        image = face_recognition.load_image_file(path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(person_name)

last_seen = {}
last_name = "-"
last_time = time.strftime("%Y-%m-%d %H:%M:%S")
last_detected_timestamp = time.time()

# -------------------------------------------------------------
# FUNGSI: STREAM VIDEO + DETEKSI WAJAH REAL-TIME
# -------------------------------------------------------------
def generate_frames():
    global last_name, last_time, last_detected_timestamp

    while True:
        success, frame = camera.read()
        if not success:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        if face_encodings:
            last_detected_timestamp = time.time()

        for face_encoding, face_location in zip(face_encodings, face_locations):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.45)
            name = "Tidak Dikenal"
            if True in matches:
                match_index = matches.index(True)
                name = known_face_names[match_index]

            now = time.time()
            if name not in last_seen or (now - last_seen[name]) > 5:
                try:
                    requests.post("http://localhost/facereconigtion/php/presensi.php", data={"nama": name})
                    last_seen[name] = now
                except:
                    pass

            top, right, bottom, left = face_location
            color = (0, 255, 0) if name != "Tidak Dikenal" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            last_name = name
            last_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Reset nama jika tidak ada wajah selama 5 detik
        if not face_encodings and time.time() - last_detected_timestamp > 5:
            last_name = "-"
            last_time = time.strftime("%Y-%m-%d %H:%M:%S")

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

# -------------------------------------------------------------
# ROUTES FLASK
# -------------------------------------------------------------
@app.route('/')
def index():
    return render_template('recognition_view.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/terakhir')
def terakhir():
    return json.dumps({"nama": last_name, "waktu": last_time})

# -------------------------------------------------------------
# ROUTE UNTUK KIRIM PERINTAH KE ESP32 VIA MQTT
# -------------------------------------------------------------
@app.route('/buka_pintu', methods=['POST'])
def buka_pintu():
    try:
        client = mqtt.Client()
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"✅ Terhubung ke broker {MQTT_BROKER}:{MQTT_PORT}")

        # 1️⃣ Kirim status "galih=BUKA"
        client.publish(MQTT_TOPIC, "galih=BUKA")
        print(f"📡 MQTT publish: galih=BUKA → topik {MQTT_TOPIC}")

        # 2️⃣ Tunggu 10 detik (galih terbuka)
        time.sleep(10)

        # 3️⃣ Kirim status "galih=TUTUP"
        client.publish(MQTT_TOPIC, "galih=TUTUP")
        print(f"📡 MQTT publish: galih=TUTUP → topik {MQTT_TOPIC}")

        client.disconnect()

        return json.dumps({
            "status": "OK",
            "pesan": "galih dibuka selama 10 detik, lalu ditutup otomatis."
        })
    except Exception as e:
        print(f"❌ Gagal MQTT: {e}")
        return json.dumps({
            "status": "ERROR",
            "pesan": f"Gagal mengirim MQTT: {e}"
        })

# -------------------------------------------------------------
# MAIN
# -------------------------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
