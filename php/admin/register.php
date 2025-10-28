<?php
include 'koneksi.php';
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
  $nama = $_POST['nama'];
  $email = $_POST['email'];
  $password = password_hash($_POST['password'], PASSWORD_DEFAULT);

  $q = "INSERT INTO admin_users (nama_lengkap, email, password) VALUES ('$nama', '$email', '$password')";
  if (mysqli_query($conn, $q)) {
    header("Location: ../../frontend/login.html");
  } else {
    echo "Gagal registrasi: " . mysqli_error($conn);
  }
}
?>
