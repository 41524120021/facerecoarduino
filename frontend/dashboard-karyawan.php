<?php
session_start();
if (!isset($_SESSION['admin'])) {
  header("Location: login-karyawan.html");
  exit();
}
?>

<!DOCTYPE html>
<html>
<head>
  <title>Dashboard Karyawan</title>
</head>
<body>
  <h2>Selamat datang, <?= $_SESSION['admin'] ?>!</h2>
  <p><a href="../php/karyawan/logout-karyawan.php">Logout</a></p>

  <h3>Daftar Karyawan</h3>
  <table border="1" cellpadding="8">
    <thead>
      <tr>
        <th>Nama</th><th>Gender</th><th>Status</th><th>Tempat Lahir</th>
        <th>Tanggal Lahir</th><th>Alamat</th><th>Kode Pos</th>
        <th>WhatsApp</th><th>Departemen</th><th>Aksi</th>
      </tr>
    </thead>
    <tbody id="userTable"></tbody>
  </table>

  <!-- Modal Edit -->
  <div id="editModal" style="display:none; position:fixed; top:20%; left:50%; transform:translateX(-50%);
    background:#fff; border:1px solid #ccc; padding:20px; z-index:1000;">
    <h3>Edit Karyawan</h3>
    <form method="POST" action="../php/karyawan/user-crud-karyawan.php">
      <input type="hidden" name="id" id="editId">
      <label>Nama:</label><br><input type="text" name="nama" id="editNama"><br>
      <label>Gender:</label><br><input type="text" name="gender" id="editGender"><br>
      <label>Status:</label><br><input type="text" name="status" id="editStatus"><br>
      <label>Tempat Lahir:</label><br><input type="text" name="tempat_lahir" id="editTempatLahir"><br>
      <label>Tanggal Lahir:</label><br><input type="text" name="tanggal_lahir" id="editTanggalLahir"><br>
      <label>Alamat:</label><br><input type="text" name="alamat" id="editAlamat"><br>
      <label>Kode Pos:</label><br><input type="text" name="kode_pos" id="editKodePos"><br>
      <label>WhatsApp:</label><br><input type="text" name="whatsapp" id="editWhatsApp"><br>
      <label>Departemen:</label><br><input type="text" name="departemen" id="editDepartemen"><br><br>
      <button type="submit" name="action" value="update">Simpan Perubahan</button>
      <button type="button" onclick="closeModal()">Batal</button>
    </form>
  </div>

  <script>
    // Fetch data dari server dan tampilkan
    fetch("../php/karyawan/get-karyawan.php")
      .then(res => res.json())
      .then(data => {
        const tbody = document.getElementById("userTable");
        data.forEach(user => {
          const row = document.createElement("tr");
          row.innerHTML = `
            <td>${user.nama}</td>
            <td>${user.gender}</td>
            <td>${user.status}</td>
            <td>${user.tempat_lahir}</td>
            <td>${user.tanggal_lahir}</td>
            <td>${user.alamat}</td>
            <td>${user.kode_pos}</td>
            <td>${user.whatsapp}</td>
            <td>${user.departemen}</td>
            <td>
              <button onclick="editUser(
                ${user.id},
                '${user.nama}', '${user.gender}', '${user.status}',
                '${user.tempat_lahir}', '${user.tanggal_lahir}',
                '${user.alamat}', '${user.kode_pos}',
                '${user.whatsapp}', '${user.departemen}'
              )">Edit</button>
              <button onclick="hapus(${user.id}, '${user.nama}')">Hapus</button>
            </td>`;
          tbody.appendChild(row);
        });
      });

    // Buka modal edit
    function editUser(id, nama, gender, status, tempat_lahir, tanggal_lahir, alamat, kode_pos, whatsapp, departemen) {
      document.getElementById("editId").value = id;
      document.getElementById("editNama").value = nama;
      document.getElementById("editGender").value = gender;
      document.getElementById("editStatus").value = status;
      document.getElementById("editTempatLahir").value = tempat_lahir;
      document.getElementById("editTanggalLahir").value = tanggal_lahir;
      document.getElementById("editAlamat").value = alamat;
      document.getElementById("editKodePos").value = kode_pos;
      document.getElementById("editWhatsApp").value = whatsapp;
      document.getElementById("editDepartemen").value = departemen;
      document.getElementById("editModal").style.display = "block";
    }

    function closeModal() {
      document.getElementById("editModal").style.display = "none";
    }

    // Hapus data + folder dataset
    function hapus(id, nama) {
      if (confirm(`Hapus user ${nama}? Ini juga akan menghapus data wajah.`)) {
        fetch(`../php/karyawan/user-crud-karyawan.php?action=delete&id=${id}&nama=${encodeURIComponent(nama)}`)
          .then(() => location.reload());
      }
    }
  </script>
</body>
</html>
