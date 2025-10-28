<?php
include 'koneksi.php';
session_start();

$email = $_POST['email'];
$password = $_POST['password'];

$q = "SELECT * FROM admin_users WHERE email='$email'";
$res = mysqli_query($conn, $q);
$row = mysqli_fetch_assoc($res);

if ($row && password_verify($password, $row['password'])) {
  $_SESSION['admin'] = $row['nama_lengkap'];
  header("Location: ../../frontend/dashboard-karyawan.php");
} else {
  echo "Login gagal";
}
?>
