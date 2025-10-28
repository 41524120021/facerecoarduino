<?php
date_default_timezone_set("Asia/Jakarta");
session_start();
if (!isset($_SESSION)) $_SESSION = [];

if (!isset($_SESSION['nama'])) $_SESSION['nama'] = "-";
if (!isset($_SESSION['waktu'])) $_SESSION['waktu'] = date("Y-m-d H:i:s");

echo json_encode([
  "nama" => $_SESSION['nama'],
  "waktu" => date("Y-m-d H:i:s")
]);
?>
