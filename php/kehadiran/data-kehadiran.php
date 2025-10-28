<?php
header('Content-Type: application/json');
include 'koneksi.php';

date_default_timezone_set('Asia/Jakarta');

$today = date('Y-m-d');

// Ambil kehadiran hari ini (tanpa duplikat nama dan tanpa "Tidak Dikenal")
$q1 = "SELECT COUNT(DISTINCT nama) as total FROM kehadiran 
       WHERE DATE(waktu) = '$today' AND nama != 'Tidak Dikenal'";
$r1 = mysqli_query($conn, $q1);
$total_hari_ini = 0;
if ($row = mysqli_fetch_assoc($r1)) {
  $total_hari_ini = (int)$row['total'];
}

// Ambil data 7 hari terakhir untuk grafik harian (tanpa "Tidak Dikenal")
$q2 = "SELECT DATE(waktu) as tanggal, COUNT(DISTINCT nama) as jumlah
       FROM kehadiran
       WHERE nama != 'Tidak Dikenal'
       GROUP BY DATE(waktu)
       ORDER BY tanggal DESC
       LIMIT 7";
$r2 = mysqli_query($conn, $q2);
$harian = [];
while ($row = mysqli_fetch_assoc($r2)) {
  $harian[] = [
    'tanggal' => $row['tanggal'],
    'jumlah' => (int)$row['jumlah']
  ];
}

// Ambil data 4 minggu terakhir untuk grafik mingguan (tanpa "Tidak Dikenal")
$q3 = "SELECT WEEK(waktu, 1) as minggu_ke, COUNT(DISTINCT nama, DATE(waktu)) as jumlah
       FROM kehadiran
       WHERE nama != 'Tidak Dikenal'
       GROUP BY WEEK(waktu, 1)
       ORDER BY minggu_ke DESC
       LIMIT 4";
$r3 = mysqli_query($conn, $q3);
$mingguan = [];
while ($row = mysqli_fetch_assoc($r3)) {
  $mingguan[] = [
    'minggu' => 'Minggu ' . $row['minggu_ke'],
    'jumlah' => (int)$row['jumlah']
  ];
}

// Ambil data detail kehadiran (semua data, kecuali "Tidak Dikenal")
/*
$q4 = "SELECT nama, waktu FROM kehadiran 
       WHERE nama != 'Tidak Dikenal' 
       ORDER BY waktu DESC 
       LIMIT 100";
$r4 = mysqli_query($conn, $q4);
$detail = [];
while ($row = mysqli_fetch_assoc($r4)) {
  $tanggal = date('Y-m-d', strtotime($row['waktu']));
  $jam     = date('H:i:s', strtotime($row['waktu']));
  $detail[] = [
    'nama' => $row['nama'],
    'tanggal' => $tanggal,
    'waktu' => $jam
  ];
}
*/

// Ambil data detail kehadiran unik per nama per hari (tanpa "Tidak Dikenal")
$q4 = "SELECT nama, DATE(waktu) as tanggal, MIN(TIME(waktu)) as waktu 
       FROM kehadiran 
       WHERE nama != 'Tidak Dikenal' 
       GROUP BY nama, DATE(waktu)
       ORDER BY tanggal DESC 
       LIMIT 100";
$r4 = mysqli_query($conn, $q4);
$detail = [];
while ($row = mysqli_fetch_assoc($r4)) {
  $detail[] = [
    'nama' => $row['nama'],
    'tanggal' => $row['tanggal'],
    'waktu' => $row['waktu']
  ];
}


// Keluarkan data JSON
echo json_encode([
  'total_hari_ini' => $total_hari_ini,
  'harian' => $harian,
  'mingguan' => $mingguan,
  'detail' => $detail
]);
?>
