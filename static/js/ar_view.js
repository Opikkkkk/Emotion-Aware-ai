function startAR() {
    // 1. Ambil elemen
    const cameraFeed = document.getElementById("camera-feed");
    const btn = document.getElementById("btn-ar");
    const statusText = document.getElementById("ar-status");

    // 2. Ubah tampilan (Simulasi menyalakan kamera)
    btn.innerText = "⏳ Menghubungkan Kamera...";
    btn.disabled = true;

    // 3. Delay sedikit seolah-olah loading
    setTimeout(() => {
        btn.style.display = "none"; // Hilangkan tombol
        cameraFeed.style.display = "flex"; // Munculkan layar kamera
        
        // Opsional: Meminta akses kamera beneran (Browser akan minta izin)
        // navigator.mediaDevices.getUserMedia({ video: true })
        //     .then(stream => {
        //         // Jika ingin canggih, stream video bisa dimasukkan ke sini
        //         // Tapi untuk prototype, kotak hitam animasi saja sudah cukup.
        //         console.log("Kamera aktif (Simulasi)");
        //     })
        //     .catch(err => {
        //         console.log("Gagal akses kamera, menggunakan simulasi.");
        //     });

    }, 1000); // Tunggu 1 detik
}