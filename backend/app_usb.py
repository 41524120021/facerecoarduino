# =============================================================
# APP_USB.PY — Sistem Face Recognition + Kontrol Pintu via USB SERIAL
# =============================================================
# Fitur:
#  - Deteksi wajah menggunakan camera (OpenCV + face_recognition)
#  - Jika wajah dikenal → tombol "Buka Pintu" aktif di web
#  - Saat ditekan → kirim pesan USB Serial ke ESP32:
#       pintu=BUKA  → LED ESP32 ON, Relay ON (10 detik)
#       pintu=TUTUP → LED ESP32 OFF, Relay OFF
# 
# Kecepatan: INSTANT (tidak perlu MQTT broker)
# =============================================================

from flask import Flask, render_template, Response, request, jsonify
import cv2
import face_recognition
import os
import requests
import time
import json
import serial
from threading import Thread

# Coba import library serial kita (jika ada)
try:
    from esp32_serial import ESP32SerialController
    USE_CUSTOM_SERIAL = True
except ImportError:
    USE_CUSTOM_SERIAL = False
    print("⚠️  esp32_serial tidak ditemukan, menggunakan standard pyserial")

# ============================================================
# KONFIGURASI UTAMA
# ============================================================
app = Flask(__name__)
camera = cv2.VideoCapture(0)

DATASET_PATH = "../dataset"        # Folder dataset wajah
SERIAL_PORT = "COM3"               # COM port ESP32 (ubah sesuai port Anda)
SERIAL_BAUDRATE = 115200           # Baud rate

# ============================================================
# GLOBAL VARIABLES
# ============================================================
esp32_controller = None
serial_connected = False

# ============================================================
# MUAT SEMUA DATASET WAJAH YANG DIKENAL
# ============================================================
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

# ============================================================
# INISIALISASI SERIAL CONNECTION
# ============================================================
def init_serial_connection():
    """Inisialisasi koneksi serial ke ESP32"""
    global esp32_controller, serial_connected
    
    try:
        if USE_CUSTOM_SERIAL:
            esp32_controller = ESP32SerialController(SERIAL_PORT, SERIAL_BAUDRATE)
            if esp32_controller.open():
                serial_connected = True
                print(f"✅ Serial {SERIAL_PORT} terhubung!")
                return True
        else:
            # Gunakan pyserial langsung
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            time.sleep(2)
            serial_connected = True
            print(f"✅ Serial {SERIAL_PORT} terhubung!")
            return True
    except Exception as e:
        serial_connected = False
        print(f"❌ Gagal connect ke serial {SERIAL_PORT}: {e}")
        print(f"   Tips: Pastikan ESP32 sudah terhubung via USB ke {SERIAL_PORT}")
        return False

# ============================================================
# FUNGSI: STREAM VIDEO + DETEKSI WAJAH REAL-TIME
# ============================================================
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

# ============================================================
# ROUTES FLASK
# ============================================================
@app.route('/')
def index():
    return render_template('recognition_view.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/terakhir')
def terakhir():
    return json.dumps({"nama": last_name, "waktu": last_time})

# ============================================================
# ROUTE UNTUK KONTROL PINTU VIA USB SERIAL
# ============================================================
@app.route('/buka_pintu', methods=['POST'])
def buka_pintu():
    global serial_connected
    
    if not serial_connected:
        return jsonify({
            "status": "ERROR",
            "pesan": f"ESP32 tidak terhubung via serial {SERIAL_PORT}. Cek USB connection!"
        }), 500
    
    try:
        print("🔓 Membuka pintu...")
        
        if USE_CUSTOM_SERIAL and esp32_controller:
            # Gunakan library custom
            esp32_controller.send_command("pintu=BUKA")
            
            # Baca response
            responses = esp32_controller.read_response(10)
            
            return jsonify({
                "status": "OK",
                "pesan": "Pintu dibuka selama 10 detik, lalu ditutup otomatis.",
                "response": responses
            })
        else:
            # Gunakan pyserial langsung
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            ser.write(b"pintu=BUKA\n")
            time.sleep(10.5)  # Tunggu 10 detik + buffer
            ser.close()
            
            return jsonify({
                "status": "OK",
                "pesan": "Pintu dibuka selama 10 detik, lalu ditutup otomatis."
            })
            
    except Exception as e:
        print(f"❌ Error: {e}")
        serial_connected = False
        return jsonify({
            "status": "ERROR",
            "pesan": f"Gagal kontrol pintu: {str(e)}"
        }), 500

@app.route('/tutup_pintu', methods=['POST'])
def tutup_pintu():
    """Tutup pintu immediate (manual)"""
    global serial_connected
    
    if not serial_connected:
        return jsonify({
            "status": "ERROR",
            "pesan": f"ESP32 tidak terhubung"
        }), 500
    
    try:
        print("🔒 Menutup pintu...")
        
        if USE_CUSTOM_SERIAL and esp32_controller:
            esp32_controller.send_command("pintu=TUTUP")
            responses = esp32_controller.read_response(3)
            
            return jsonify({
                "status": "OK",
                "pesan": "Pintu ditutup",
                "response": responses
            })
        else:
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            ser.write(b"pintu=TUTUP\n")
            time.sleep(1)
            ser.close()
            
            return jsonify({
                "status": "OK",
                "pesan": "Pintu ditutup"
            })
            
    except Exception as e:
        serial_connected = False
        return jsonify({
            "status": "ERROR",
            "pesan": f"Gagal kontrol pintu: {str(e)}"
        }), 500

@app.route('/serial_status', methods=['GET'])
def serial_status():
    """Cek status koneksi serial"""
    return jsonify({
        "connected": serial_connected,
        "port": SERIAL_PORT,
        "baudrate": SERIAL_BAUDRATE
    })

@app.route('/test_led', methods=['POST'])
def test_led():
    """Test LED via serial"""
    if not serial_connected:
        return jsonify({"status": "ERROR", "pesan": "ESP32 tidak terhubung"}), 500
    
    try:
        if USE_CUSTOM_SERIAL and esp32_controller:
            esp32_controller.send_command("test=LED")
        else:
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            ser.write(b"test=LED\n")
            ser.close()
        
        return jsonify({"status": "OK", "pesan": "Test LED sent"})
    except Exception as e:
        return jsonify({"status": "ERROR", "pesan": str(e)}), 500

@app.route('/test_relay', methods=['POST'])
def test_relay():
    """Test Relay via serial"""
    if not serial_connected:
        return jsonify({"status": "ERROR", "pesan": "ESP32 tidak terhubung"}), 500
    
    try:
        if USE_CUSTOM_SERIAL and esp32_controller:
            esp32_controller.send_command("test=RELAY")
        else:
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            ser.write(b"test=RELAY\n")
            ser.close()
        
        return jsonify({"status": "OK", "pesan": "Test RELAY sent"})
    except Exception as e:
        return jsonify({"status": "ERROR", "pesan": str(e)}), 500

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print()
    print("╔═══════════════════════════════════════════════════╗")
    print("║   Face Recognition + USB Serial Door Control    ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()
    
    # Inisialisasi koneksi serial
    if init_serial_connection():
        print("✅ Siap digunakan!\n")
    else:
        print("⚠️  Jalankan tanpa koneksi serial. Cek USB connection!\n")
    
    # Jalankan Flask
    app.run(debug=True, host='127.0.0.1', port=5000)
