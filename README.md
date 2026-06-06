# Kablo İzolasyon Ölçüm Sistemi

Bu proje, görüntü işleme tabanlı bir kablo izolasyon kalınlığı ölçüm sistemidir. Özellikle çok damarlı (3 delikli) kablolar üzerinde dış çap, iç çap, eksen kaçıklığı ve izolasyon kalınlığı ölçümlerini otomatik olarak yapar.

## Özellikler

- OpenCV ile görüntü işleme (Model Ekleme/Genişletme destekli Mimari)
- FastAPI tabanlı yüksek performanslı arka uç
- Modern Glassmorphism Web Arayüzü (HTML/CSS/JS)
- JSON raporu dışa aktarabilme
- Docker desteği

## Kurulum ve Çalıştırma

### Yöntem 1: Docker ile Çalıştırma (Önerilen)

Sisteminizde Docker yüklü ise aşağıdaki komutlarla projeyi çalıştırabilirsiniz:

```bash
docker build -t cable-inspection .
docker run -p 8000:8000 cable-inspection
```

Tarayıcınızdan `http://localhost:8000` adresine giderek arayüze ulaşabilirsiniz.

### Yöntem 2: Python Ortamında Çalıştırma

Gerekli paketleri kurun (Python 3.9+ önerilir):

```bash
pip install -r requirements.txt
```

Uygulamayı başlatın:

```bash
python main.py
```

Tarayıcınızdan `http://localhost:8000` adresine giderek arayüze ulaşabilirsiniz.

## Kullanım
1. Arayüzden **Görüntü Al** butonuna tıklayıp örnek bir kesit görüntüsü (örn: `uc_damarli_1.jpg`) seçin.
2. Diğer giriş parametrelerini (Piksel-mm Katsayısı vb.) isteğinize göre düzenleyin.
3. **Hesapla** butonuna tıklayın.
4. Çıkan sonuç görselini ve tabloyu inceleyin. JSON formatında almak için **Rapor Oluştur**'a tıklayın.
