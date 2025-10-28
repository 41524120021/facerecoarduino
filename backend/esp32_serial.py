"""
=============================================================
ESP32 USB Serial Communication Library
=============================================================
Library untuk berkomunikasi dengan ESP32 via USB Serial
untuk kontrol LED dan Relay (bypass MQTT)

Penggunaan:
    from esp32_serial import ESP32SerialController
    
    esp32 = ESP32SerialController('COM3', 115200)
    esp32.open()
    esp32.send_command('pintu=BUKA')
    response = esp32.read_response()
    esp32.close()
"""

import serial
import time
import logging
from typing import Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ESP32SerialController:
    """
    Kontrol ESP32 via USB Serial (bukan MQTT)
    """
    
    def __init__(self, port: str, baudrate: int = 115200, timeout: float = 2.0):
        """
        Inisialisasi koneksi serial
        
        Args:
            port: COM port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate: Baud rate (default 115200)
            timeout: Timeout untuk read (default 2 detik)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.ser = None
        self.connected = False
    
    def open(self) -> bool:
        """
        Buka koneksi serial ke ESP32
        
        Returns:
            True jika berhasil, False jika gagal
        """
        try:
            self.ser = serial.Serial(
                port=self.port,
                baudrate=self.baudrate,
                timeout=self.timeout,
                write_timeout=self.timeout
            )
            time.sleep(2)  # Tunggu ESP32 initialize setelah serial open
            self.connected = True
            logger.info(f"✅ Serial {self.port} dibuka (baudrate: {self.baudrate})")
            return True
        except Exception as e:
            logger.error(f"❌ Gagal buka serial {self.port}: {e}")
            self.connected = False
            return False
    
    def close(self):
        """Tutup koneksi serial"""
        if self.ser and self.ser.is_open:
            self.ser.close()
            self.connected = False
            logger.info(f"Serial {self.port} ditutup")
    
    def send_command(self, command: str) -> bool:
        """
        Kirim perintah ke ESP32
        
        Args:
            command: Perintah (e.g., 'pintu=BUKA', 'test=LED')
        
        Returns:
            True jika berhasil, False jika gagal
        """
        if not self.connected or not self.ser or not self.ser.is_open:
            logger.error("❌ Serial tidak terhubung!")
            return False
        
        try:
            # Tambah newline di akhir untuk Serial.readStringUntil('\n')
            self.ser.write(f"{command}\n".encode('utf-8'))
            logger.info(f"📤 Kirim: {command}")
            return True
        except Exception as e:
            logger.error(f"❌ Gagal kirim perintah: {e}")
            return False
    
    def read_response(self, lines: int = 5) -> list:
        """
        Baca response dari ESP32
        
        Args:
            lines: Jumlah baris yang dibaca (default 5)
        
        Returns:
            List berisi baris-baris response
        """
        if not self.connected or not self.ser or not self.ser.is_open:
            logger.error("❌ Serial tidak terhubung!")
            return []
        
        responses = []
        try:
            for _ in range(lines):
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8').strip()
                    if line:
                        responses.append(line)
                        logger.info(f"📥 Response: {line}")
                else:
                    break
            return responses
        except Exception as e:
            logger.error(f"❌ Gagal baca response: {e}")
            return []
    
    def send_and_read(self, command: str, lines: int = 5) -> list:
        """
        Kirim perintah dan langsung baca response
        
        Args:
            command: Perintah yang dikirim
            lines: Jumlah baris response yang dibaca
        
        Returns:
            List response
        """
        if self.send_command(command):
            time.sleep(0.5)  # Tunggu ESP32 process
            return self.read_response(lines)
        return []
    
    def buka_pintu(self, wait_for_completion: bool = True) -> bool:
        """
        Buka pintu (LED ON, Relay ON selama 10 detik)
        
        Args:
            wait_for_completion: Tunggu sampai selesai (10 detik)
        
        Returns:
            True jika berhasil, False jika gagal
        """
        logger.info("🔓 Membuka pintu...")
        responses = self.send_and_read('pintu=BUKA', lines=10)
        
        if wait_for_completion:
            logger.info("⏳ Tunggu 10 detik untuk pintu menutup otomatis...")
            time.sleep(10)
        
        return len(responses) > 0
    
    def tutup_pintu(self) -> bool:
        """
        Tutup pintu (LED OFF, Relay OFF immediately)
        
        Returns:
            True jika berhasil, False jika gagal
        """
        logger.info("🔒 Menutup pintu...")
        responses = self.send_and_read('pintu=TUTUP', lines=3)
        return len(responses) > 0
    
    def test_led(self) -> bool:
        """Test LED blink"""
        logger.info("🧪 Test LED...")
        responses = self.send_and_read('test=LED', lines=2)
        return len(responses) > 0
    
    def test_relay(self) -> bool:
        """Test Relay ON 2 detik"""
        logger.info("🧪 Test RELAY...")
        responses = self.send_and_read('test=RELAY', lines=2)
        return len(responses) > 0
    
    def get_status(self) -> dict:
        """
        Dapatkan status LED dan Relay
        
        Returns:
            Dict berisi status {'led': 'ON'/'OFF', 'relay': 'ON'/'OFF'}
        """
        responses = self.send_and_read('status', lines=5)
        status = {'led': 'UNKNOWN', 'relay': 'UNKNOWN'}
        
        for line in responses:
            if 'LED:' in line:
                status['led'] = 'ON' if 'ON' in line else 'OFF'
            elif 'RELAY:' in line:
                status['relay'] = 'ON' if 'ON' in line else 'OFF'
        
        logger.info(f"Status: LED={status['led']}, RELAY={status['relay']}")
        return status


# =============================================================
# CONTOH PENGGUNAAN
# =============================================================
if __name__ == '__main__':
    # Inisialisasi ESP32 serial controller
    esp32 = ESP32SerialController('COM3', 115200)  # Ganti COM3 sesuai port Anda
    
    # Buka koneksi
    if esp32.open():
        print("\n✅ Koneksi berhasil!\n")
        
        # Test 1: Get Status
        print("=== TEST 1: GET STATUS ===")
        esp32.get_status()
        time.sleep(1)
        
        # Test 2: Test LED
        print("\n=== TEST 2: TEST LED ===")
        esp32.test_led()
        time.sleep(2)
        
        # Test 3: Test RELAY
        print("\n=== TEST 3: TEST RELAY ===")
        esp32.test_relay()
        time.sleep(3)
        
        # Test 4: Buka Pintu
        print("\n=== TEST 4: BUKA PINTU ===")
        esp32.buka_pintu(wait_for_completion=False)
        
        # Tutup koneksi
        esp32.close()
        print("\n✅ Test selesai!")
    else:
        print("❌ Gagal membuka koneksi serial!")
