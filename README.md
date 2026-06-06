# Cable Insulation Measurement System (Kablo İzolasyon Ölçüm Sistemi)

Bu proje, görüntü işleme tabanlı bir **kablo izolasyon kalınlığı ölçüm** sistemidir. OpenCV ve Python kullanarak, kablo kesit görüntülerinden mikrometre hassasiyetinde ölçümler alır ve bunu modern bir web arayüzünde kullanıcılara sunar.

## 🚀 Desteklenen Kablo Tipleri ve Analiz Algoritmaları

Proje, Endüstri 4.0 ve kalite kontrol standartlarına uygun olarak tasarlanmış 3 ayrı görüntü işleme algoritması barındırır:

1. **Tek Damarlı (Som Telli) - `SingleCoreAnalyzer`**
   - İçi tamamen dolu, tek parça bakır veya alüminyum iletkenli kabloları ölçer.
2. **Tek Damarlı (Çok Telli) - `MultiStrandedAnalyzer`**
   - İçerisinde çok sayıda ince tel (strand) bulunan kabloları ölçer. Telleri **Dışbükey Örtü (Convex Hull)** mantığıyla sarıp tek bir merkez çıkartır.
3. **Çok Damarlı (3 Delikli vb.) - `ThreeCoreAnalyzer`**
   - İçerisinde birden fazla kalın damar (veya yonca biçimli yapışık damarlar) barındıran kabloları ölçer. Geometrik kusurları (Convexity Defects) tespit ederek yapışık damarları analiz edebilir.

## 🧠 Teknik Yetenekler (Computer Vision)
- **Robust HSV Eşikleme:** Standart Siyah-Beyaz filtrenin yanılgıya düştüğü "Beyaz arkaplanlı sarı kablolar" gibi zorlu koşullarda, Renk Doygunluğu (Saturation) ve Ters Parlaklık (Inverted Value) kullanarak %100 başarıyla dış sınır tespiti.
- **Hata Yakalama (Mismatch Handling):** Seçilen kablo tipi ile yüklenen görsel eşleşmezse (Örn: Çok telli seçip 3 delikli resim yükleme), sistem bunu anlayarak **REST API** üzerinden kullanıcıya anlamlı hatalar fırlatır.
- **Detaylı Raporlama:** Dış/İç çap, 6 farklı açıda izolasyon kalınlığı, min/max/ort kalınlık ve Öklid eksen kaçıklığı (Eccentricity) hesabı.

## 💻 Kurulum ve Çalıştırma

Proje **Docker** ortamına tamamen uyumludur. Hızlı bir şekilde ayağa kaldırmak için:

```bash
# 1. Projeyi İndirin
git clone https://github.com/zkoc1/Cable-Insulation-Measurement-.git
cd Cable-Insulation-Measurement-

# 2. Docker İmajını Derleyin
docker build -t cable-inspection .

# 3. Docker Konteynerini Başlatın
docker run -p 8000:8000 cable-inspection
```
Tarayıcınızdan `http://localhost:8000` adresine giderek arayüze ulaşabilirsiniz.

### Python Ortamında Çalıştırma (Geliştiriciler İçin)
```bash
pip install -r requirements.txt
python main.py
```

## 📸 Kullanım (Demo Adımları)
1. Arayüzden kablo tipini seçin.
2. Piksel-mm katsayınızı girin. (Örn: `0.02`)
3. **Dosya Seç** diyerek kesit görselini (Örn: `som_telli_1.jpg`, `cok_telli_1.jpg`, `uc_damarli_1.jpg`) seçin.
4. **Hesapla** butonuna tıklayın.
5. Sonuç tablosu ve çizimli analiz görseli saniyeler içerisinde karşınızda olacaktır. Çıktıyı JSON formatında elde etmek için **Rapor Oluştur** butonuna tıklayabilirsiniz.
