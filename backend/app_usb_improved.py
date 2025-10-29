# =============================================================
# APP_USB.PY — Face Recognition + USB Serial Door Control (IMPROVED)
# =============================================================
# Fitur:
#  - Deteksi wajah menggunakan camera (OpenCV + face_recognition)
#  - Jika wajah dikenal → tombol "Buka Pintu" aktif di web
#  - Saat ditekan → kirim pesan USB Serial ke ESP32:
#       pintu=BUKA  → LED ESP32 ON, Relay ON (10 detik)
#       pintu=TUTUP → LED ESP32 OFF, Relay OFF
# 
# Perbaikan:
#  - Better error handling pada dataset loading
#  - Tunable tolerance untuk face matching
#  - Detailed logging untuk debug
#  - Face distance calculation untuk confidence score
# =============================================================

from flask import Flask, render_template, Response, request, jsonify
import cv2
import face_recognition
import os
import requests
import time
import json
import numpy as np
from threading import Thread

# Coba import library serial kita
try:
    from esp32_serial import ESP32SerialController
    USE_CUSTOM_SERIAL = True
except ImportError:
    USE_CUSTOM_SERIAL = False
    print("⚠️  esp32_serial tidak ditemukan, menggunakan standard pyserial")
    import serial

# ============================================================
# KONFIGURASI
# ============================================================
app = Flask(__name__)

# Initialize camera later (in generate_frames) untuk avoid blocking
camera = None

DATASET_PATH = "../dataset"
SERIAL_PORT = "COM3"
SERIAL_BAUDRATE = 115200

# TUNING PARAMETERS
FACE_TOLERANCE = 0.5  # 0.6 = lebih permisif, 0.4 = lebih ketat
FACE_DETECTION_MODEL = "hog"  # "hog" (cepat) atau "cnn" (akurat tapi lambat)
NUM_JITTERS = 1  # Berapa kali process face untuk accuracy (1=cepat, 2+=lebih akurat)

# ============================================================
# GLOBAL VARIABLES
# ============================================================
esp32_controller = None
serial_connected = False

# Dataset dan face encodings
known_face_encodings = []
known_face_names = []
known_face_files = []  # Track file source untuk debugging

last_seen = {}
last_name = "-"
last_time = time.strftime("%Y-%m-%d %H:%M:%S")
last_detected_timestamp = time.time()

# Statistics
stats = {
    "faces_detected": 0,
    "faces_recognized": 0,
    "total_encodings": 0
}

# ============================================================
# MUAT DATASET WAJAH
# ============================================================
def load_dataset():
    """Load semua face encodings dari dataset folder"""
    global known_face_encodings, known_face_names, known_face_files
    
    print()
    print("=" * 60)
    print("📁 LOADING FACE ENCODINGS FROM DATASET")
    print("=" * 60)
    
    if not os.path.exists(DATASET_PATH):
        print(f"⚠️  Dataset folder NOT FOUND: {DATASET_PATH}")
        print(f"    App akan berjalan tanpa face recognition")
        return
    
    total_files = 0
    total_loaded = 0
    
    try:
        for person_name in sorted(os.listdir(DATASET_PATH)):
            folder = os.path.join(DATASET_PATH, person_name)
            if not os.path.isdir(folder):
                continue
            
            person_count = 0
            print(f"\n👤 Processing: {person_name}")
            
            for file in os.listdir(folder):
                if not file.lower().endswith(('.jpg', '.jpeg', '.png')):
                    continue
                
                total_files += 1
                path = os.path.join(folder, file)
                
                try:
                    # Load image
                    print(f"   Loading {file}...", end=" ", flush=True)
                    image = face_recognition.load_image_file(path)
                    
                    # Extract face encodings
                    face_locations = face_recognition.face_locations(image, model=FACE_DETECTION_MODEL)
                    face_encodings = face_recognition.face_encodings(image, face_locations, num_jitters=NUM_JITTERS)
                    
                    if face_encodings:
                        # Add first face encoding
                        known_face_encodings.append(face_encodings[0])
                        known_face_names.append(person_name)
                        known_face_files.append(file)
                        person_count += 1
                        total_loaded += 1
                        print("✅")
                    else:
                        print("⚠️  (no faces detected)")
                        
                except Exception as e:
                    print(f"❌ ({str(e)[:30]})")
                    continue
            
            print(f"   ✅ {person_name}: {person_count} encodings")
        
        print()
        print("=" * 60)
        print(f"✅ DATASET LOADED SUCCESSFULLY")
        print(f"   Total files: {total_files}")
        print(f"   Total encodings: {total_loaded}")
        print(f"   Unique persons: {len(set(known_face_names))}")
        print(f"   Persons: {', '.join(sorted(set(known_face_names)))}")
        print("=" * 60)
        print()
        
        stats["total_encodings"] = total_loaded
        
    except Exception as e:
        print(f"❌ ERROR loading dataset: {e}")
        import traceback
        traceback.print_exc()

# Load dataset on startup
load_dataset()

# ============================================================
# INISIALISASI SERIAL
# ============================================================
def init_serial_connection():
    """Inisialisasi koneksi serial ke ESP32"""
    global esp32_controller, serial_connected
    
    try:
        if USE_CUSTOM_SERIAL:
            esp32_controller = ESP32SerialController(SERIAL_PORT, SERIAL_BAUDRATE)
            if esp32_controller.open():
                serial_connected = True
                print(f"✅ Serial {SERIAL_PORT} connected!")
                return True
        else:
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            time.sleep(2)
            serial_connected = True
            print(f"✅ Serial {SERIAL_PORT} connected!")
            return True
    except KeyboardInterrupt:
        print("⚠️  Serial init interrupted by user")
        return False
    except Exception as e:
        serial_connected = False
        print(f"❌ Gagal connect ke serial {SERIAL_PORT}: {e}")
        return False

# ============================================================
# GENERATE VIDEO FRAMES WITH FACE DETECTION
# ============================================================
def generate_frames():
    global last_name, last_time, last_detected_timestamp, stats, camera
    
    # Initialize camera on first call
    if camera is None:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            print("⚠️  Camera not available!")
            return

    frame_count = 0
    skip_frames = 0  # Skip every N frames untuk speed
    
    while True:
        success, frame = camera.read()
        if not success:
            break

        frame_count += 1
        
        # Resize frame untuk speed
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        # Only process every 2 frames untuk speed
        if frame_count % 2 == 0:
            try:
                # Detect faces
                face_locations = face_recognition.face_locations(rgb_small_frame, model=FACE_DETECTION_MODEL)
                face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations, num_jitters=NUM_JITTERS)
                
                if face_encodings:
                    last_detected_timestamp = time.time()
                    stats["faces_detected"] = len(face_encodings)
                
                face_names = []
                face_distances = []
                
                for face_encoding in face_encodings:
                    # Compare dengan known faces
                    distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                    
                    if len(distances) > 0:
                        # Get best match
                        best_match_index = np.argmin(distances)
                        best_distance = distances[best_match_index]
                        
                        # Check jika match threshold
                        if best_distance < FACE_TOLERANCE:
                            name = known_face_names[best_match_index]
                            stats["faces_recognized"] += 1
                        else:
                            name = "Tidak Dikenal"
                    else:
                        name = "Tidak Dikenal"
                    
                    face_names.append(name)
                    face_distances.append(best_distance if len(distances) > 0 else 1.0)
                
                # Update last detected person
                if face_names and face_names[0] != "Tidak Dikenal":
                    last_name = face_names[0]
                    last_time = time.strftime("%Y-%m-%d %H:%M:%S")
                    
                    # Log to presensi
                    now = time.time()
                    if last_name not in last_seen or (now - last_seen[last_name]) > 5:
                        try:
                            requests.post("http://localhost/facereconigtion/php/presensi.php", 
                                        data={"nama": last_name}, timeout=1)
                            last_seen[last_name] = now
                        except:
                            pass
                        
            except Exception as e:
                print(f"⚠️  Face detection error: {e}")
        
        # Reset jika tidak ada wajah selama 5 detik
        if not face_encodings and time.time() - last_detected_timestamp > 5:
            last_name = "-"
            last_time = time.strftime("%Y-%m-%d %H:%M:%S")
        
        # Draw detected faces pada ORIGINAL FRAME (full size)
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back to original frame
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4
            
            color = (0, 255, 0) if name != "Tidak Dikenal" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
        
        # Encode untuk streaming
        _, buffer = cv2.imencode('.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 80])
        frame_bytes = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

# ============================================================
# ROUTES
# ============================================================
@app.route('/')
def index():
    return render_template('recognition_view_usb.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/terakhir')
def terakhir():
    return json.dumps({"nama": last_name, "waktu": last_time})

@app.route('/stats')
def get_stats():
    return jsonify(stats)

# ============================================================
# KONTROL PINTU
# ============================================================
@app.route('/buka_pintu', methods=['POST'])
def buka_pintu():
    global serial_connected
    
    if not serial_connected:
        return jsonify({
            "status": "ERROR",
            "pesan": f"ESP32 tidak terhubung via serial {SERIAL_PORT}"
        }), 500
    
    try:
        print("🔓 Opening door...")
        
        if USE_CUSTOM_SERIAL and esp32_controller:
            esp32_controller.send_command("pintu=BUKA")
            responses = esp32_controller.read_response(10)
            return jsonify({
                "status": "OK",
                "pesan": "Pintu dibuka selama 10 detik",
                "response": responses
            })
        else:
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            ser.write(b"pintu=BUKA\n")
            time.sleep(10.5)
            ser.close()
            return jsonify({
                "status": "OK",
                "pesan": "Pintu dibuka selama 10 detik, lalu ditutup otomatis."
            })
            
    except Exception as e:
        serial_connected = False
        return jsonify({
            "status": "ERROR",
            "pesan": f"Gagal kontrol pintu: {str(e)}"
        }), 500

@app.route('/tutup_pintu', methods=['POST'])
def tutup_pintu():
    global serial_connected
    
    if not serial_connected:
        return jsonify({"status": "ERROR", "pesan": "ESP32 tidak terhubung"}), 500
    
    try:
        print("🔒 Closing door...")
        
        if USE_CUSTOM_SERIAL and esp32_controller:
            esp32_controller.send_command("pintu=TUTUP")
            responses = esp32_controller.read_response(3)
            return jsonify({"status": "OK", "pesan": "Pintu ditutup", "response": responses})
        else:
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            ser.write(b"pintu=TUTUP\n")
            time.sleep(1)
            ser.close()
            return jsonify({"status": "OK", "pesan": "Pintu ditutup"})
            
    except Exception as e:
        serial_connected = False
        return jsonify({"status": "ERROR", "pesan": f"Gagal kontrol pintu: {str(e)}"})

@app.route('/serial_status', methods=['GET'])
def serial_status():
    return jsonify({
        "connected": serial_connected,
        "port": SERIAL_PORT,
        "baudrate": SERIAL_BAUDRATE
    })

@app.route('/test_led', methods=['POST'])
def test_led():
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
    print("║              (IMPROVED VERSION)                  ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()
    print(f"🔧 Configuration:")
    print(f"   Dataset: {DATASET_PATH}")
    print(f"   Serial: {SERIAL_PORT} @ {SERIAL_BAUDRATE} baud")
    print(f"   Tolerance: {FACE_TOLERANCE} (lower=stricter)")
    print(f"   Detection Model: {FACE_DETECTION_MODEL}")
    print()
    
    # Inisialisasi serial
    if init_serial_connection():
        print("✅ Ready to use!\n")
    else:
        print("⚠️  Running without serial connection. Check USB!\n")
    
    # Jalankan Flask
    print("🚀 Starting Flask...")
    print("📍 Open: http://127.0.0.1:5001")
    print()
    app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False, threaded=True)
