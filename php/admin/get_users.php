<?php
include 'koneksi.php';
$q = "SELECT id, nama_lengkap, email FROM admin_users";
$res = mysqli_query($conn, $q);
$data = [];
while ($row = mysqli_fetch_assoc($res)) {
  $data[] = $row;
}
echo json_encode($data);
?>
