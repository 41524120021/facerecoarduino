# Face Recognition Attendance System - Setup Guide

## 📋 Instalasi Database

### 1. Buat Database MySQL
Jalankan file SQL untuk membuat database dan tabel:

**Menggunakan phpMyAdmin:**
1. Buka http://localhost/phpmyadmin
2. Klik tab **SQL**
3. Copy isi file `database_setup.sql`
4. Paste dan klik **Go**

**Menggunakan MySQL CLI:**
```powershell
# Navigate ke MySQL bin folder
cd C:\xampp\mysql\bin

# Login ke MySQL
.\mysql.exe -u root -p
# Tekan Enter jika tidak ada password

# Jalankan SQL file
source D:/xampp/htdocs/facereconigtion/database_setup.sql;
```

### 2. Login Admin Default
Setelah database dibuat, gunakan kredensial ini:
- **Email:** admin@face.com
- **Password:** admin123

---

## 🐍 Instalasi Python Backend

### 1. Pastikan Virtual Environment Aktif
Virtual environment sudah dibuat di `.venv/`

### 2. Install Dependencies
```powershell
cd D:\xampp\htdocs\facereconigtion\backend
D:/xampp/htdocs/facereconigtion/.venv/Scripts/pip.exe install -r requirements.txt
```

### 3. Jalankan Aplikasi Flask
```powershell
cd D:\xampp\htdocs\facereconigtion\backend
D:/xampp/htdocs/facereconigtion/.venv/Scripts/python.exe app.py
```

**Catatan:** 
- Aplikasi akan memuat face encodings dari folder `dataset/` (bisa memakan waktu)
- Pastikan webcam tidak digunakan oleh aplikasi lain
- Tunggu hingga muncul pesan: `* Running on http://127.0.0.1:5000`

### 4. Akses Aplikasi
Buka browser: http://127.0.0.1:5000

---

## 📁 Struktur Folder Dataset

Tambahkan foto wajah karyawan di folder `dataset/`:
```
dataset/
  ├── Nama_Karyawan_1/
  │   ├── foto1.jpg
  │   ├── foto2.jpg
  │   └── foto3.jpg
  ├── Nama_Karyawan_2/
  │   ├── foto1.jpg
  │   └── foto2.jpg
```

**Tips:**
- Gunakan 3-5 foto per orang dengan berbagai ekspresi dan pencahayaan
- Format: JPG atau PNG
- Nama folder = nama yang akan muncul di sistem

---

## 🔧 Konfigurasi MQTT (ESP32)

Edit `backend/app.py` jika perlu mengubah:
- **MQTT_BROKER:** "broker.hivemq.com" (default)
- **MQTT_PORT:** 1883
- **MQTT_TOPIC:** "fc/galih"

---

## ⚙️ Troubleshooting

### Error: `ModuleNotFoundError`
Pastikan semua dependencies terinstall:
```powershell
D:/xampp/htdocs/facereconigtion/.venv/Scripts/pip.exe list
```

### Error: `Table 'admin_users' doesn't exist`
Jalankan ulang `database_setup.sql`

### Webcam tidak terdeteksi
- Pastikan webcam terhubung
- Cek apakah aplikasi lain menggunakan webcam
- Coba ubah `camera = cv2.VideoCapture(0)` ke `VideoCapture(1)` di `app.py`

### Face recognition lambat
- Kurangi jumlah foto di dataset
- Gunakan foto dengan resolusi lebih kecil (maks 800x800px)

---

## 📞 Support

Untuk masalah lebih lanjut, periksa:
- Log error di terminal Flask
- Log PHP di XAMPP Control Panel
- phpMyAdmin untuk verifikasi database
