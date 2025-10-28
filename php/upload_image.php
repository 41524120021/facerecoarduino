<?php
// upload_image.php
// Menyimpan snapshot ke folder images dan dataset berdasarkan nama lengkap

$data = json_decode(file_get_contents("php://input"), true);
$image = $data['image'] ?? '';
$name = $data['name'] ?? '';

if (!$image || !$name) {
    echo "Gagal: Data gambar atau nama kosong.";
    exit;
}

$folder_name = str_replace(' ', '_', $name);
$path_images = "../images/" . $folder_name;
$path_dataset = "../dataset/" . $folder_name;

if (!file_exists($path_images)) mkdir($path_images, 0777, true);
if (!file_exists($path_dataset)) mkdir($path_dataset, 0777, true);

// Hitung file sebelumnya, supaya nama file tidak duplikat
$image_count = count(glob($path_images . "/*.jpg"));
$filename = "img_" . ($image_count + 1) . ".jpg";

// Konversi base64 → binary
$image = str_replace('data:image/jpeg;base64,', '', $image);
$image = str_replace(' ', '+', $image);
$decoded = base64_decode($image);

// Simpan ke dua lokasi
file_put_contents($path_images . "/" . $filename, $decoded);
file_put_contents($path_dataset . "/" . $filename, $decoded);

echo "Berhasil disimpan: $filename";
?>
