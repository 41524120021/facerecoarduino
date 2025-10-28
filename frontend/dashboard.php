<?php
session_start();
if (!isset($_SESSION['admin'])) {
  header("Location: login.html");
  exit();
}
?>

<!DOCTYPE html>
<html>
<head><title>Dashboard Admin</title></head>
<body>
  <h2>Selamat datang, <?= $_SESSION['admin'] ?>!</h2>
  <p><a href="../php/admin/logout.php">Logout</a></p>
  <h3>Daftar User Admin</h3>
  <table border="1" cellpadding="8">
    <thead><tr><th>Nama</th><th>Email</th><th>Aksi</th></tr></thead>
    <tbody id="userTable"></tbody>
  </table>

  <div id="editModal" style="display:none; position:fixed; top:20%; left:50%; transform:translateX(-50%);
    background:#fff; border:1px solid #ccc; padding:20px; z-index:1000;">
    <h3>Edit Admin</h3>
    <form method="POST" action="../php/admin/user_crud.php">
      <input type="hidden" name="id" id="editId">
      <label>Nama:</label><br>
      <input type="text" name="nama" id="editNama"><br>
      <label>Email:</label><br>
      <input type="email" name="email" id="editEmail"><br><br>
      <button type="submit" name="action" value="update">Simpan Perubahan</button>
      <button type="button" onclick="closeModal()">Batal</button>
    </form>
  </div>

  <div id="passwordModal" style="display:none; position:fixed; top:30%; left:50%; transform:translateX(-50%);
    background:#fff; border:1px solid #ccc; padding:20px; z-index:1000;">
    <h3>Ubah Password</h3>
    <form method="POST" action="../php/admin/user_crud.php">
      <input type="hidden" name="id" id="passwordUserId">
      <label>Password Baru:</label><br>
      <input type="password" name="new_password" required><br><br>
      <button type="submit" name="action" value="update_password">Simpan</button>
      <button type="button" onclick="closePasswordModal()">Batal</button>
    </form>
  </div>





  <script>
    fetch("../php/admin/get_users.php")
      .then(res => res.json())
      .then(data => {
        const tbody = document.getElementById("userTable");
        data.forEach(user => {
          const row = document.createElement("tr");
          row.innerHTML = `<td>${user.nama_lengkap}</td><td>${user.email}</td>
            <td>
              <button onclick="editUser(${user.id}, '${user.nama_lengkap}', '${user.email}')">Edit</button>
              <button onclick="showPasswordModal(${user.id})">Ubah Password</button>
              <button onclick="hapus(${user.id})">Hapus</button>
            </td>`;
          tbody.appendChild(row);
        });
      });

    function hapus(id) {
      if (confirm("Hapus user ini?")) {
        fetch("../php/admin/user_crud.php?action=delete&id=" + id)
          .then(() => location.reload());
      }
    }

    function editUser(id, nama, email) {
      document.getElementById("editId").value = id;
      document.getElementById("editNama").value = nama;
      document.getElementById("editEmail").value = email;
      document.getElementById("editModal").style.display = "block";
    }

    function closeModal() {
      document.getElementById("editModal").style.display = "none";
    }    

    function showPasswordModal(id) {
      document.getElementById("passwordUserId").value = id;
      document.getElementById("passwordModal").style.display = "block";
    }

    function closePasswordModal() {
      document.getElementById("passwordModal").style.display = "none";
    }

  </script>
</body>
</html>
