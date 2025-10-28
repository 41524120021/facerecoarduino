<?php
include '../koneksi.php';

$action = $_POST['action'] ?? $_GET['action'] ?? '';
$id     = $_POST['id'] ?? $_GET['id'] ?? '';
$nama   = $_POST['nama'] ?? $_GET['nama'] ?? '';

if ($action == 'update') {
  $gender = $_POST['gender'];
  $status = $_POST['status'];
  $tempat_lahir = $_POST['tempat_lahir'];
  $tanggal_lahir = $_POST['tanggal_lahir'];
  $alamat = $_POST['alamat'];
  $kode_pos = $_POST['kode_pos'];
  $whatsapp = $_POST['whatsapp'];
  $departemen = $_POST['departemen'];

  $q = "UPDATE anggota SET
        nama='$nama', gender='$gender', status='$status',
        tempat_lahir='$tempat_lahir', tanggal_lahir='$tanggal_lahir',
        alamat='$alamat', kode_pos='$kode_pos', whatsapp='$whatsapp',
        departemen='$departemen'
        WHERE id='$id'";
  mysqli_query($conn, $q) or die(mysqli_error($conn));
  header("Location: ../../dashboard-karyawan.php");
}

if ($action == 'delete') {
  mysqli_query($conn, "DELETE FROM anggota WHERE id='$id'");

  // Hapus folder dataset
  $folder1 = "../../dataset/$nama";
  $folder2 = "../../images/$nama";
  function deleteFolder($folder) {
    if (is_dir($folder)) {
      $files = scandir($folder);
      foreach ($files as $file) {
        if ($file !== "." && $file !== "..") {
          unlink("$folder/$file");
        }
      }
      rmdir($folder);
    }
  }

  deleteFolder($folder1);
  deleteFolder($folder2);

  echo "Deleted";
}
?>
