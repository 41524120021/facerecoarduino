-- =============================================================
-- DATABASE SETUP - Face Attendance System
-- =============================================================
-- Instruksi:
-- 1. Buka phpMyAdmin: http://localhost/phpmyadmin
-- 2. Buat database baru bernama 'face_attendance' (jika belum ada)
-- 3. Pilih database 'face_attendance'
-- 4. Klik tab SQL
-- 5. Copy paste script ini dan klik Go
-- =============================================================

-- Hapus database lama jika ada (HATI-HATI: ini akan menghapus semua data)
-- DROP DATABASE IF EXISTS face_attendance;

-- Buat database baru
CREATE DATABASE IF NOT EXISTS `face_attendance` 
  DEFAULT CHARACTER SET utf8mb4 
  COLLATE utf8mb4_unicode_ci;

USE `face_attendance`;

-- =============================================================
-- TABEL: admin_users
-- Menyimpan data admin aplikasi
-- =============================================================
CREATE TABLE IF NOT EXISTS `admin_users` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nama_lengkap` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- TABEL: karyawan (jika diperlukan)
-- Menyimpan data karyawan
-- =============================================================
CREATE TABLE IF NOT EXISTS `karyawan` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nama_lengkap` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL UNIQUE,
  `password` VARCHAR(255) NOT NULL,
  `jabatan` VARCHAR(100) DEFAULT NULL,
  `created_at` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` TIMESTAMP NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- TABEL: presensi
-- Menyimpan data kehadiran karyawan
-- =============================================================
CREATE TABLE IF NOT EXISTS `presensi` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `nama` VARCHAR(255) NOT NULL,
  `waktu` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `status` ENUM('Hadir', 'Tidak Dikenal') DEFAULT 'Hadir',
  INDEX `idx_nama` (`nama`),
  INDEX `idx_waktu` (`waktu`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- DATA AWAL (SEED)
-- Contoh admin pertama dengan password: admin123
-- =============================================================
-- Password hash untuk 'admin123'
INSERT INTO `admin_users` (`nama_lengkap`, `email`, `password`) 
VALUES ('Administrator', 'admin@face.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi')
ON DUPLICATE KEY UPDATE `nama_lengkap` = 'Administrator';

-- =============================================================
-- VERIFIKASI
-- =============================================================
SELECT 'Database setup completed successfully!' AS Status;
SELECT 'Tables created:' AS Info;
SHOW TABLES;
