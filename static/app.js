document.addEventListener("DOMContentLoaded", () => {
    const btnCapture = document.getElementById("btnCapture");
    const btnCalculate = document.getElementById("btnCalculate");
    const btnRefresh = document.getElementById("btnRefresh");
    const btnReport = document.getElementById("btnReport");
    const imageUpload = document.getElementById("imageUpload");
    
    const resultImage = document.getElementById("resultImage");
    const imagePlaceholder = document.getElementById("imagePlaceholder");
    const resultsTable = document.getElementById("resultsTable");
    const resultsBody = document.getElementById("resultsBody");
    
    let currentData = null;

    btnCapture.addEventListener("click", () => {
        imageUpload.click();
    });

    imageUpload.addEventListener("change", (e) => {
        if (e.target.files && e.target.files[0]) {
            const reader = new FileReader();
            reader.onload = (e) => {
                resultImage.src = e.target.result;
                resultImage.style.display = "block";
                imagePlaceholder.style.display = "none";
                btnCapture.disabled = true;
                btnCapture.textContent = "Görüntü Seçildi";
            };
            reader.readAsDataURL(e.target.files[0]);
        }
    });

    document.getElementById("controlForm").addEventListener("submit", async (e) => {
        e.preventDefault();
        
        if (!imageUpload.files[0]) {
            alert("Lütfen önce bir görüntü seçin (Görüntü Al)");
            return;
        }

        const formData = new FormData();
        formData.append("file", imageUpload.files[0]);
        formData.append("cable_type", document.getElementById("cableType").value);
        formData.append("pixel_to_mm", document.getElementById("pixelToMm").value);

        btnCalculate.disabled = true;
        btnCalculate.textContent = "Hesaplanıyor...";

        try {
            const response = await fetch("/api/measure", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                throw new Error("Sunucu hatası");
            }

            const data = await response.json();
            currentData = data;
            
            resultImage.src = data.result_image_url;
            
            resultsBody.innerHTML = "";
            const parameters = [
                { key: "Görüntü Adı", val: data.image_name },
                { key: "Dış Merkez (px)", val: `[${data.outer_center_px.join(', ')}]` },
                { key: "İç Merkez (px)", val: `[${data.inner_center_px.join(', ')}]` },
                { key: "Dış Çap", val: `${data.outer_diameter_mm.toFixed(2)} mm` },
                { key: "İç Çap", val: `${data.inner_diameter_mm.toFixed(2)} mm` },
                { key: "Min Kalınlık", val: `${data.min_thickness_mm.toFixed(2)} mm` },
                { key: "Max Kalınlık", val: `${data.max_thickness_mm.toFixed(2)} mm` },
                { key: "Ortalama Kalınlık", val: `${data.mean_thickness_mm.toFixed(2)} mm` },
                { key: "Eksen Kaçıklığı", val: `${data.eccentricity_mm.toFixed(2)} mm` }
            ];

            parameters.forEach(p => {
                const tr = document.createElement("tr");
                tr.innerHTML = `<td>${p.key}</td><td>${p.val}</td>`;
                resultsBody.appendChild(tr);
            });

            resultsTable.style.display = "table";
            btnReport.disabled = false;

        } catch (error) {
            alert("Hesaplama sırasında bir hata oluştu: " + error.message);
        } finally {
            btnCalculate.disabled = false;
            btnCalculate.textContent = "Hesapla";
        }
    });

    btnRefresh.addEventListener("click", () => {
        document.getElementById("controlForm").reset();
        resultImage.style.display = "none";
        imagePlaceholder.style.display = "block";
        resultsTable.style.display = "none";
        resultsBody.innerHTML = "";
        btnReport.disabled = true;
        btnCapture.disabled = false;
        btnCapture.textContent = "Görüntü Al";
        currentData = null;
    });

    btnReport.addEventListener("click", () => {
        if (!currentData) return;
        const jsonStr = JSON.stringify(currentData, null, 2);
        const blob = new Blob([jsonStr], { type: "application/json" });
        const url = URL.createObjectURL(blob);
        const a = document.createElement("a");
        a.href = url;
        a.download = "olcum_raporu.json";
        a.click();
        URL.revokeObjectURL(url);
    });
});
