<?php
include 'koneksi.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['action'] == 'update') {
  $id = $_POST['id'];
  $nama = $_POST['nama'];
  $email = $_POST['email'];

  $q = "UPDATE admin_users SET nama_lengkap='$nama', email='$email' WHERE id=$id";
  mysqli_query($conn, $q);
  header("Location: ../../frontend/dashboard.php");
  exit();
}

if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_POST['action'] == 'update_password') {
  $id = $_POST['id'];
  $new_password = password_hash($_POST['new_password'], PASSWORD_DEFAULT);
  mysqli_query($conn, "UPDATE admin_users SET password='$new_password' WHERE id=$id");
  header("Location: ../../frontend/dashboard.php");
  exit();
}

if ($_GET['action'] == 'delete') {
  $id = $_GET['id'];
  mysqli_query($conn, "DELETE FROM admin_users WHERE id=$id");
}
?>
