# 🚀 Cara Menjalankan Aplikasi Face Recognition

## ⚠️ PENTING: Urutan Menjalankan Aplikasi

Aplikasi ini terdiri dari 2 bagian yang harus berjalan bersamaan:
1. **Flask Backend** (Python) - Port 5000
2. **Apache/XAMPP Frontend** (PHP) - Port 80

---

## 📝 Langkah-langkah Setup

### 1️⃣ Setup Database (Hanya Sekali)

**Buka phpMyAdmin:**
```
http://localhost/phpmyadmin
```

**Jalankan SQL:**
1. Klik tab **SQL**
2. Copy paste isi file `database_setup.sql`
3. Klik **Go**

---

### 2️⃣ Jalankan Flask Backend (WAJIB)

**Buka Terminal/PowerShell:**

```powershell
# Navigasi ke folder backend
cd D:\xampp\htdocs\facereconigtion\backend

# Jalankan Flask app
D:/xampp/htdocs/facereconigtion/.venv/Scripts/python.exe app.py
```

**Tunggu sampai muncul:**
```
* Running on http://127.0.0.1:5000
```

**⚠️ JANGAN TUTUP terminal ini!** Flask harus tetap berjalan.

---

### 3️⃣ Akses Aplikasi

Ada 2 cara mengakses aplikasi:

#### **Opsi A: Langsung Flask (Rekomendasi untuk Face Recognition)**
```
http://127.0.0.1:5000
```
- ✅ Video streaming langsung dari Flask
- ✅ Realtime face detection
- ✅ Tombol buka pintu (MQTT ke ESP32)

#### **Opsi B: Melalui Frontend PHP (untuk Admin Dashboard)**
```
http://localhost/facereconigtion/frontend/face-recognition.html
```
- ✅ UI lebih baik dengan error handling
- ⚠️ Butuh Flask tetap running di background
- ✅ Bisa akses dari browser lain dalam network

**Dashboard Admin:**
```
http://localhost/facereconigtion/frontend/dashboard.php
```

---

## 🔧 Troubleshooting

### ❌ Error: "404 Not Found" atau "CORS Error"

**Penyebab:** Flask server belum jalan atau salah URL

**Solusi:**
1. Pastikan Flask running di terminal
2. Cek apakah ada tulisan `* Running on http://127.0.0.1:5000`
3. Akses langsung: http://127.0.0.1:5000
4. Jangan gunakan `localhost` untuk Flask, pakai `127.0.0.1`

---

### ❌ Error: "Video feed tidak muncul"

**Penyebab:** 
- Webcam tidak terdeteksi
- Flask masih loading dataset
- Webcam digunakan aplikasi lain

**Solusi:**
1. Tutup aplikasi yang menggunakan webcam (Zoom, Skype, dll)
2. Tunggu Flask selesai load face encodings (bisa 30-60 detik)
3. Cek terminal Flask untuk error
4. Ubah camera index di `app.py`:
   ```python
   camera = cv2.VideoCapture(0)  # coba ganti 0 jadi 1
   ```

---

### ❌ Error: "Table 'admin_users' doesn't exist"

**Penyebab:** Database belum dibuat

**Solusi:**
1. Buka phpMyAdmin: http://localhost/phpmyadmin
2. Jalankan file `database_setup.sql`

---

### ❌ Error: "ModuleNotFoundError"

**Penyebab:** Python packages belum terinstall

**Solusi:**
```powershell
cd D:\xampp\htdocs\facereconigtion\backend
D:/xampp/htdocs/facereconigtion/.venv/Scripts/pip.exe install -r requirements.txt
```

---

## 📱 Akses dari HP/Device Lain

### 1. Cari IP Komputer:
```powershell
ipconfig
```
Cari **IPv4 Address**, misalnya: `192.168.1.100`

### 2. Edit `app.py`:
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
```

### 3. Akses dari HP:
```
http://192.168.1.100:5000
```

### 4. Update `frontend/face-recognition.html`:
Ganti:
```javascript
const FLASK_URL = 'http://192.168.1.100:5000';  // IP komputer kamu
```

---

## 🎯 Flow Penggunaan Normal

1. **Start Flask:**
   ```powershell
   cd D:\xampp\htdocs\facereconigtion\backend
   D:/xampp/htdocs/facereconigtion/.venv/Scripts/python.exe app.py
   ```

2. **Tunggu loading dataset** (30-60 detik)

3. **Buka browser:**
   ```
   http://127.0.0.1:5000
   ```

4. **Wajah terdeteksi** → Tombol "Buka Pintu" aktif

5. **Klik tombol** → ESP32 terima MQTT → Pintu buka 10 detik

---

## 🔐 Login Default

**Admin:**
- Email: `admin@face.com`
- Password: `admin123`

---

## 📊 Port yang Digunakan

- **Flask Backend:** `5000`
- **Apache/PHP:** `80`
- **MySQL:** `3306`
- **MQTT Broker:** `broker.hivemq.com:1883`

---

## ⏹️ Cara Stop Aplikasi

1. **Stop Flask:** Tekan `Ctrl + C` di terminal Flask
2. **Stop Apache:** XAMPP Control Panel → Stop Apache
3. **Stop MySQL:** XAMPP Control Panel → Stop MySQL

---

## 💡 Tips

- ✅ Selalu jalankan Flask terlebih dahulu
- ✅ Gunakan `127.0.0.1:5000` bukan `localhost:5000` untuk Flask
- ✅ Pastikan webcam tidak digunakan aplikasi lain
- ✅ Dataset foto sebaiknya 3-5 foto per orang
- ✅ Foto harus jelas, pencahayaan bagus
- ✅ Jangan tekan Ctrl+C saat Flask loading dataset

---

## 📞 Bantuan

Jika masih error, cek:
1. **Terminal Flask** - lihat error message
2. **Browser Console** (F12) - lihat error JavaScript
3. **Apache Error Log** - `xampp/apache/logs/error.log`
4. **MySQL Error Log** - `xampp/mysql/data/*.err`
