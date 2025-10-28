<?php
include 'koneksi.php';
$q = "SELECT id, nama, gender, status, tempat_lahir, tanggal_lahir, alamat, kode_pos, whatsapp, departemen FROM anggota";
$res = mysqli_query($conn, $q);
$data = [];
while ($row = mysqli_fetch_assoc($res)) {
  $data[] = $row;
}
echo json_encode($data);
?>
