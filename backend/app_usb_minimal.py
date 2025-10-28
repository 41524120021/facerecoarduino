# =============================================================
# APP_USB_MINIMAL.PY — Face Recognition + Kontrol Pintu (Cepat Load)
# =============================================================
# Versi minimal yang TIDAK load dataset di startup
# Dataset loaded on-demand atau disampling saja
# =============================================================

from flask import Flask, render_template, Response, request, jsonify
import cv2
import os
import time
import json
from threading import Thread
import sys

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
camera = cv2.VideoCapture(0)

DATASET_PATH = "../dataset"
SERIAL_PORT = "COM3"
SERIAL_BAUDRATE = 115200

# ============================================================
# GLOBAL VARIABLES
# ============================================================
esp32_controller = None
serial_connected = False

# Placeholder untuk face recognition (skip loading)
known_face_encodings = []
known_face_names = []

last_name = "-"
last_time = time.strftime("%Y-%m-%d %H:%M:%S")
last_detected_timestamp = time.time()

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
                print(f"✅ Serial {SERIAL_PORT} terhubung!")
                return True
        else:
            ser = serial.Serial(SERIAL_PORT, SERIAL_BAUDRATE, timeout=2)
            time.sleep(2)
            serial_connected = True
            print(f"✅ Serial {SERIAL_PORT} terhubung!")
            return True
    except Exception as e:
        serial_connected = False
        print(f"❌ Gagal connect ke serial {SERIAL_PORT}: {e}")
        return False

# ============================================================
# GENERATE FRAMES - SIMPLE VERSION (NO FACE RECOGNITION)
# ============================================================
def generate_frames():
    global last_name, last_time, last_detected_timestamp

    while True:
        success, frame = camera.read()
        if not success:
            break

        # Buat simple output tanpa face detection terlebih dahulu
        cv2.putText(frame, f"Last: {last_name} | {last_time}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

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
        print("🔓 Membuka pintu...")
        
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
    print("║              (MINIMAL VERSION - FAST LOAD)       ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()
    
    # Inisialisasi koneksi serial
    if init_serial_connection():
        print("✅ Siap digunakan!\n")
    else:
        print("⚠️  Jalankan tanpa koneksi serial. Cek USB connection!\n")
    
    # Jalankan Flask di port 5001
    print("📍 Running on http://127.0.0.1:5001")
    print()
    app.run(debug=False, host='127.0.0.1', port=5001, use_reloader=False)
