<?php
include 'koneksi.php';
$id = $_POST['id'];
$nama = $_POST['nama'];
$gender = $_POST['gender'];
$status = $_POST['status'];
$tempat = $_POST['tempat'];
$tgl = $_POST['tgl'];
$alamat = $_POST['alamat'];
$kodepos = $_POST['kodepos'];
$wa = $_POST['wa'];
$departemen = $_POST['departemen'];
$folder = str_replace(' ', '_', $nama);
$path = "../images/$folder";
if (!file_exists($path)) mkdir($path, 0777, true);
$q = "INSERT INTO anggota (id, nama, gender, status, tempat_lahir, tanggal_lahir, alamat, kode_pos, whatsapp, departemen, folder)
VALUES ('$id', '$nama', '$gender', '$status', '$tempat', '$tgl', '$alamat', '$kodepos', '$wa', '$departemen', '$folder')";
echo mysqli_query($conn, $q) ? "Data berhasil disimpan." : "Gagal menyimpan: " . mysqli_error($conn);
?>