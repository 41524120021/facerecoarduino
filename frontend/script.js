// script.js
const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({ video: true })
  .then((stream) => { video.srcObject = stream; })
  .catch((err) => { console.error("Webcam error:", err); });

let capturedImages = []; // Array penampung gambar base64

function takeSnapshot() {
  const canvas = document.createElement("canvas");
  canvas.width = video.videoWidth;
  canvas.height = video.videoHeight;
  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, canvas.width, canvas.height);
  const imageDataUrl = canvas.toDataURL("image/jpeg");
  const img = document.createElement("img");
  img.src = imageDataUrl;
  img.alt = "Snapshot";
  document.getElementById("thumbnails").appendChild(img);
  capturedImages.push(imageDataUrl); // Simpan untuk nanti dikirim saat form submit
}

// Saat form dikirim → simpan semua gambar ke server
document.getElementById("dataForm").addEventListener("submit", function (e) {
  e.preventDefault(); // hentikan submit default dulu

  const form = e.target;
  const formData = new FormData(form);
  const name = formData.get("nama");

  // Simpan data ke database via PHP
  fetch(form.action, {
    method: "POST",
    body: formData
  })
  .then(res => res.text())
  .then(msg => {
    console.log("Data form:", msg);

    // Kirim semua gambar ke server (upload_image.php)
    capturedImages.forEach(imageData => {
      fetch("../php/upload_image.php", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ image: imageData, name: name })
      })
      .then(res => res.text())
      .then(status => console.log("Gambar:", status))
      .catch(err => console.error("Upload Gagal:", err));
    });

    alert("Data dan gambar berhasil dikirim!");
    form.reset();
    document.getElementById("thumbnails").innerHTML = "";
    capturedImages = [];
  });
});