#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_esp32_web.py - Simple Flask Web Interface untuk Test ESP32 USB Serial
Tanpa face recognition, hanya untuk test LED, Relay, dan Door Control
"""

from flask import Flask, render_template, jsonify, request
import time
import os
from esp32_serial import ESP32SerialController

app = Flask(__name__)

# ============================================================
# KONFIGURASI
# ============================================================
SERIAL_PORT = "COM3"           # Ubah sesuai port Anda
SERIAL_BAUDRATE = 115200

# Global variable untuk status
esp32_controller = None
serial_connected = False

# ============================================================
# INISIALISASI SERIAL CONNECTION
# ============================================================
def init_serial_connection():
    """Inisialisasi koneksi serial ke ESP32"""
    global esp32_controller, serial_connected
    
    try:
        esp32_controller = ESP32SerialController(SERIAL_PORT, SERIAL_BAUDRATE)
        if esp32_controller.open():
            serial_connected = True
            print(f"✅ Serial {SERIAL_PORT} terhubung!")
            return True
        else:
            serial_connected = False
            print(f"❌ Gagal connect ke serial {SERIAL_PORT}")
            return False
    except Exception as e:
        serial_connected = False
        print(f"❌ Exception: {e}")
        return False

# ============================================================
# ROUTES
# ============================================================

@app.route('/')
def index():
    """Main page"""
    return '''
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>ESP32 USB Serial Test</title>
        <style>
            * {
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
            }
            .container {
                background: white;
                border-radius: 15px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
                max-width: 600px;
                width: 100%;
                padding: 40px;
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
                border-bottom: 3px solid #667eea;
                padding-bottom: 20px;
            }
            .header h1 {
                color: #333;
                font-size: 2em;
                margin-bottom: 10px;
            }
            .header p {
                color: #666;
                font-size: 1em;
            }
            .status-bar {
                background: #f8f9fa;
                padding: 15px 20px;
                border-radius: 10px;
                margin-bottom: 30px;
                display: flex;
                align-items: center;
                gap: 15px;
            }
            .status-indicator {
                width: 16px;
                height: 16px;
                border-radius: 50%;
                background-color: #dc3545;
                animation: pulse 1s infinite;
            }
            .status-indicator.connected {
                background-color: #28a745;
                animation: none;
            }
            @keyframes pulse {
                0%, 100% { opacity: 1; }
                50% { opacity: 0.5; }
            }
            .status-text {
                flex: 1;
                font-size: 1em;
                color: #555;
                font-weight: 500;
            }
            .controls {
                display: grid;
                gap: 15px;
            }
            .control-group {
                display: flex;
                gap: 10px;
            }
            .btn {
                flex: 1;
                padding: 15px 20px;
                border: none;
                border-radius: 8px;
                font-size: 1em;
                font-weight: 600;
                cursor: pointer;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .btn:disabled {
                opacity: 0.5;
                cursor: not-allowed;
            }
            .btn-primary {
                background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
                color: white;
            }
            .btn-primary:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(40, 167, 69, 0.3);
            }
            .btn-danger {
                background: linear-gradient(135deg, #dc3545 0%, #e74c3c 100%);
                color: white;
            }
            .btn-danger:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(220, 53, 69, 0.3);
            }
            .btn-secondary {
                background: linear-gradient(135deg, #6c757d 0%, #5a6268 100%);
                color: white;
                font-size: 0.9em;
            }
            .btn-secondary:hover:not(:disabled) {
                transform: translateY(-2px);
                box-shadow: 0 8px 20px rgba(108, 117, 125, 0.3);
            }
            .alert {
                padding: 15px 20px;
                border-radius: 8px;
                margin-bottom: 15px;
                display: none;
                animation: slideIn 0.3s ease;
            }
            @keyframes slideIn {
                from {
                    opacity: 0;
                    transform: translateY(-10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            .alert.show {
                display: block;
            }
            .alert-success {
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }
            .alert-error {
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }
            .info-box {
                background: #f8f9fa;
                padding: 15px 20px;
                border-radius: 8px;
                margin-top: 30px;
                border-left: 4px solid #667eea;
            }
            .info-box h3 {
                color: #333;
                margin-bottom: 10px;
                font-size: 1.1em;
            }
            .info-box p {
                color: #666;
                font-size: 0.95em;
                line-height: 1.6;
            }
            .info-box code {
                background: white;
                padding: 2px 6px;
                border-radius: 3px;
                font-family: 'Courier New', monospace;
                color: #d63384;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🔐 ESP32 USB Serial Control</h1>
                <p>Test LED, Relay, dan Door Control</p>
            </div>

            <!-- Status Bar -->
            <div class="status-bar">
                <div class="status-indicator" id="statusIndicator"></div>
                <span class="status-text">Status: <strong id="statusText">Checking...</strong></span>
            </div>

            <!-- Alert Messages -->
            <div id="alert" class="alert"></div>

            <!-- Controls -->
            <div class="controls">
                <!-- Door Control -->
                <div class="control-group">
                    <button class="btn btn-primary" id="bukaBtn" onclick="bukapintu()" disabled>
                        🔓 Buka Pintu (10s)
                    </button>
                    <button class="btn btn-danger" id="tutupBtn" onclick="tutuppintu()" disabled>
                        🔒 Tutup Pintu
                    </button>
                </div>

                <!-- Test Buttons -->
                <div class="control-group">
                    <button class="btn btn-secondary" onclick="testLED()" disabled id="testLedBtn">
                        💡 Test LED
                    </button>
                    <button class="btn btn-secondary" onclick="testRelay()" disabled id="testRelayBtn">
                        ⚡ Test Relay
                    </button>
                </div>

                <!-- Refresh Status -->
                <div class="control-group">
                    <button class="btn btn-secondary" onclick="checkStatus()">
                        🔄 Refresh Status
                    </button>
                </div>
            </div>

            <!-- Info Box -->
            <div class="info-box">
                <h3>📋 Informasi</h3>
                <p><strong>Port:</strong> <code id="portInfo">COM3</code></p>
                <p><strong>Baud Rate:</strong> <code>115200</code></p>
                <p><strong>Durasi Pintu:</strong> <code>10 detik (auto-close)</code></p>
                <p style="margin-top: 10px; font-size: 0.9em; color: #999;">
                    Pastikan ESP32 sudah terhubung via USB dan Arduino sketch sudah di-upload.
                </p>
            </div>
        </div>

        <script>
            // ===== CEK STATUS SETIAP 2 DETIK =====
            function checkStatus() {
                fetch('/api/serial_status')
                    .then(res => res.json())
                    .then(data => {
                        const indicator = document.getElementById('statusIndicator');
                        const statusText = document.getElementById('statusText');
                        const testLedBtn = document.getElementById('testLedBtn');
                        const testRelayBtn = document.getElementById('testRelayBtn');
                        const bukaBtn = document.getElementById('bukaBtn');
                        const tutupBtn = document.getElementById('tutupBtn');

                        if (data.connected) {
                            indicator.classList.add('connected');
                            statusText.textContent = '✅ Terhubung';
                            statusText.style.color = '#28a745';
                            
                            testLedBtn.disabled = false;
                            testRelayBtn.disabled = false;
                            bukaBtn.disabled = false;
                            tutupBtn.disabled = false;
                        } else {
                            indicator.classList.remove('connected');
                            statusText.textContent = '❌ Terputus';
                            statusText.style.color = '#dc3545';
                            
                            testLedBtn.disabled = true;
                            testRelayBtn.disabled = true;
                            bukaBtn.disabled = true;
                            tutupBtn.disabled = true;
                            
                            showAlert('⚠️ ESP32 tidak terhubung via USB. Periksa connection!', 'error');
                        }
                    })
                    .catch(err => console.error('Status check failed:', err));
            }

            // ===== BUKA PINTU =====
            async function bukapintu() {
                const btn = document.getElementById('bukaBtn');
                btn.disabled = true;
                btn.textContent = 'Membuka... (10s)';

                try {
                    const response = await fetch('/api/buka_pintu', { method: 'POST' });
                    const data = await response.json();

                    if (data.status === 'OK') {
                        showAlert('✅ Pintu dibuka! Akan otomatis tutup dalam 10 detik.', 'success');
                        setTimeout(() => {
                            btn.disabled = false;
                            btn.textContent = '🔓 Buka Pintu (10s)';
                            checkStatus();
                        }, 10500);
                    } else {
                        showAlert('❌ ' + data.message, 'error');
                        btn.disabled = false;
                        btn.textContent = '🔓 Buka Pintu (10s)';
                    }
                } catch (error) {
                    showAlert('❌ Error: ' + error.message, 'error');
                    btn.disabled = false;
                    btn.textContent = '🔓 Buka Pintu (10s)';
                }
            }

            // ===== TUTUP PINTU =====
            async function tutuppintu() {
                try {
                    const response = await fetch('/api/tutup_pintu', { method: 'POST' });
                    const data = await response.json();

                    if (data.status === 'OK') {
                        showAlert('✅ Pintu ditutup', 'success');
                    } else {
                        showAlert('❌ ' + data.message, 'error');
                    }
                } catch (error) {
                    showAlert('❌ Error: ' + error.message, 'error');
                }
            }

            // ===== TEST LED =====
            async function testLED() {
                try {
                    await fetch('/api/test_led', { method: 'POST' });
                    showAlert('💡 Test LED dikirim! Lihat LED berkedip...', 'success');
                } catch (error) {
                    showAlert('❌ Error: ' + error.message, 'error');
                }
            }

            // ===== TEST RELAY =====
            async function testRelay() {
                try {
                    await fetch('/api/test_relay', { method: 'POST' });
                    showAlert('⚡ Test Relay dikirim! Dengarkan bunyi relay...', 'success');
                } catch (error) {
                    showAlert('❌ Error: ' + error.message, 'error');
                }
            }

            // ===== SHOW ALERT =====
            function showAlert(message, type = 'info') {
                const alertBox = document.getElementById('alert');
                alertBox.textContent = message;
                alertBox.className = `alert show alert-${type}`;
                
                setTimeout(() => {
                    alertBox.classList.remove('show');
                }, 5000);
            }

            // ===== STARTUP =====
            window.addEventListener('load', () => {
                checkStatus();
                setInterval(checkStatus, 2000);  // Check setiap 2 detik
            });
        </script>
    </body>
    </html>
    '''

@app.route('/api/buka_pintu', methods=['POST'])
def buka_pintu():
    global serial_connected
    
    if not serial_connected:
        return jsonify({
            "status": "ERROR",
            "message": f"ESP32 tidak terhubung"
        }), 500
    
    try:
        print("🔓 Buka Pintu...")
        esp32_controller.send_command("pintu=BUKA")
        responses = esp32_controller.read_response(10)
        
        return jsonify({
            "status": "OK",
            "message": "Pintu dibuka selama 10 detik",
            "response": responses
        })
    except Exception as e:
        serial_connected = False
        print(f"❌ Error: {e}")
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500

@app.route('/api/tutup_pintu', methods=['POST'])
def tutup_pintu():
    global serial_connected
    
    if not serial_connected:
        return jsonify({
            "status": "ERROR",
            "message": "ESP32 tidak terhubung"
        }), 500
    
    try:
        print("🔒 Tutup Pintu...")
        esp32_controller.send_command("pintu=TUTUP")
        responses = esp32_controller.read_response(3)
        
        return jsonify({
            "status": "OK",
            "message": "Pintu ditutup",
            "response": responses
        })
    except Exception as e:
        serial_connected = False
        return jsonify({
            "status": "ERROR",
            "message": str(e)
        }), 500

@app.route('/api/test_led', methods=['POST'])
def test_led():
    global serial_connected
    
    if not serial_connected:
        return jsonify({"status": "ERROR", "message": "ESP32 tidak terhubung"}), 500
    
    try:
        esp32_controller.send_command("test=LED")
        return jsonify({"status": "OK", "message": "Test LED sent"})
    except Exception as e:
        serial_connected = False
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/test_relay', methods=['POST'])
def test_relay():
    global serial_connected
    
    if not serial_connected:
        return jsonify({"status": "ERROR", "message": "ESP32 tidak terhubung"}), 500
    
    try:
        esp32_controller.send_command("test=RELAY")
        return jsonify({"status": "OK", "message": "Test RELAY sent"})
    except Exception as e:
        serial_connected = False
        return jsonify({"status": "ERROR", "message": str(e)}), 500

@app.route('/api/serial_status', methods=['GET'])
def serial_status():
    return jsonify({
        "connected": serial_connected,
        "port": SERIAL_PORT,
        "baudrate": SERIAL_BAUDRATE
    })

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print()
    print("╔═══════════════════════════════════════════════════╗")
    print("║   ESP32 USB Serial Test Web Interface           ║")
    print("╚═══════════════════════════════════════════════════╝")
    print()
    
    # Inisialisasi koneksi serial
    if init_serial_connection():
        print("✅ Siap digunakan!\n")
    else:
        print("⚠️  Jalankan tanpa koneksi serial. Cek USB connection!\n")
    
    # Jalankan Flask
    print("🚀 Starting Flask server...")
    print("📍 Open: http://127.0.0.1:5000")
    print()
    
    app.run(debug=True, host='127.0.0.1', port=5000)
