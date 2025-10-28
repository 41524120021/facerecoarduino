from flask import Flask, render_template, Response, request
import cv2
import face_recognition
import os
import requests
import time
import json
import paho.mqtt.client as mqtt

app = Flask(__name__)
camera = cv2.VideoCapture(0)

# ===== Konfigurasi Dataset & MQTT =====
DATASET_PATH = "../dataset"
# MQTT_BROKER = "localhost"     # Ganti dengan IP broker MQTT Anda (misalnya: "192.168.1.10")
MQTT_BROKER = "broker.hivemq.com"     # Ganti dengan IP broker MQTT Anda (misalnya: "192.168.1.10")
MQTT_PORT = 1883
MQTT_TOPIC = "esp32/pintu"

known_face_encodings = []
known_face_names = []

# ===== Muat semua wajah yang dikenal =====
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

# ===== Fungsi utama streaming video + deteksi wajah =====
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
                    requests.post("http://localhost/007-face-recognition-riska/005-face-recognition-iot/php/presensi.php", data={"nama": name})
                    last_seen[name] = now
                except:
                    pass

            top, right, bottom, left = face_location
            color = (0, 255, 0) if name != "Tidak Dikenal" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

            last_name = name
            last_time = time.strftime("%Y-%m-%d %H:%M:%S")

        # Jika tidak ada wajah terdeteksi selama 5 detik, reset nama
        if not face_encodings and time.time() - last_detected_timestamp > 5:
            last_name = "-"
            last_time = time.strftime("%Y-%m-%d %H:%M:%S")

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


# ===== ROUTES FLASK =====
@app.route('/')
def index():
    return render_template('recognition_view.html')


@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/terakhir')
def terakhir():
    return json.dumps({"nama": last_name, "waktu": last_time})


# ===== ROUTE UNTUK MENGIRIM PERINTAH KE ESP32 =====
@app.route('/buka_pintu', methods=['POST'])
def buka_pintu():
    try:
        client = mqtt.Client()
        print("🔌 Menghubungkan ke broker MQTT...")
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        print(f"✅ Terhubung ke broker {MQTT_BROKER}:{MQTT_PORT}")
        result = client.publish(MQTT_TOPIC, "BUKA")
        client.disconnect()

        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"📡 Pesan 'BUKA' dikirim ke topik {MQTT_TOPIC}")
            return json.dumps({"status": "OK", "pesan": "Perintah buka pintu dikirim ke ESP32 via HiveMQ!"})
        else:
            print("⚠️ MQTT publish gagal.")
            return json.dumps({"status": "ERROR", "pesan": "MQTT publish gagal."})

        # print("📡 Perintah 'BUKA' dikirim ke ESP32 melalui MQTT")
        # return json.dumps({"status": "OK", "pesan": "Perintah buka pintu dikirim ke ESP32!"})
    except Exception as e:
        print(f"❌ Gagal mengirim MQTT: {e}")
        return json.dumps({"status": "ERROR", "pesan": f"Gagal mengirim MQTT: {e}"})


if __name__ == '__main__':
    app.run(debug=True)
