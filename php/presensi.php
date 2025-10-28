<?php
include 'koneksi.php';
date_default_timezone_set('Asia/Jakarta'); // Set zona waktu

$nama = $_POST['nama'] ?? '';
if ($nama == '') { echo "Tidak Dikenal"; exit; }

$waktu = date("Y-m-d H:i:s");
$q = "INSERT INTO kehadiran (nama, waktu) VALUES ('$nama', '$waktu')";
echo mysqli_query($conn, $q) ? "Presensi dicatat untuk $nama pada $waktu" : "Gagal mencatat: " . mysqli_error($conn);
?>
