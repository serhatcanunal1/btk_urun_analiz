# 🛍️ Ürün Analiz Sistemi v2.0

## 📋 Proje Hakkında

**Bu proje BTK Yarışması için Trivox takımı tarafından geliştirilmiştir.**

**Takım Üyeleri:**
- **Serhatcan Ünal** - Proje Lideri & Backend Geliştirici
- **Elif Zeynep Tosun** - AI Uzmanı & Frontend Geliştirici  
- **Meryem Gençali** - Web Scraping Uzmanı & UI/UX Tasarımcısı

**Ürün Analiz Sistemi**, e-ticaret sitelerinden ürün verilerini toplayarak AI destekli detaylı analiz yapan gelişmiş bir web uygulamasıdır. Bu sistem, kullanıcıların bilinçli alışveriş kararları almasına yardımcı olmak için tasarlanmıştır.

### 🎯 Proje Amacı

**BTK Yarışması Kapsamında Geliştirilen Bu Proje:**
- Ürün karşılaştırmalarını objektif verilerle yapmak
- AI teknolojisi ile satın alma önerileri sunmak
- Kullanıcı yorumlarını analiz ederek duygu durumunu çıkarmak
- Çoklu platform desteği ile kapsamlı analiz yapmak

## ✨ Özellikler

### 🔍 Web Scraping
- **Çoklu Platform Desteği**: Trendyol, Amazon ve diğer e-ticaret siteleri
- **Gerçek Zamanlı Veri Çekme**: Güncel fiyat ve yorum bilgileri
- **Akıllı Yorum Toplama**: Selenium WebDriver ile dinamik içerik desteği
- **Rate Limiting**: Site politikalarına uygun veri çekme

### 🤖 AI Destekli Analiz
- **Gemini AI Entegrasyonu**: Google'ın en gelişmiş AI modeliyle analiz
- **Duygu Analizi**: Yorumların pozitif, nötr, negatif kategorilere ayrılması
- **Satın Alma Önerisi**: AI tabanlı öneriler ve güven skorları
- **Özellik Çıkarımı**: Ürün özelliklerinin otomatik tespiti

### 📊 Karşılaştırma Sistemi
- **Çok Kriterli Değerlendirme**: Fiyat, kalite, kullanıcı memnuniyeti
- **AI Yorumu**: Gemini AI'ın ürünler arası tercihi ve gerekçesi
- **Görsel Skorlama**: Progress bar ile kolay anlaşılır sonuçlar
- **Detaylı Raporlama**: Her kriterde ayrıntılı analiz

### 💾 Veri Yönetimi
- **Kalıcı Saklama**: JSON formatında ürün analizleri
- **Çoklu Export**: JSON, CSV formatlarında veri aktarımı
- **Toplu İşlemler**: Tüm ürünleri tek seferde export etme
- **Veri İntegrasyonu**: Kolay veri paylaşımı ve işleme

### 🌐 Modern Web Arayüzü
- **Responsive Tasarım**: Mobil uyumlu kullanıcı arayüzü
- **Bootstrap 5**: Modern ve hızlı UI komponentleri
- **Font Awesome**: Zengin ikon seti
- **AJAX Desteği**: Sayfa yenileme olmadan işlemler

## 🏗️ Proje Yapısı

```
BTK Proje/
├── 📁 analyzer/                    # AI analiz modülleri
│   ├── __init__.py                 # Paket başlatma
│   ├── gemini_analyzer.py          # Temel Gemini AI analizi
│   └── product_detailed_analyzer.py # Detaylı ürün analizi (Ana AI modülü)
│
├── 📁 data/                        # Veri saklama dizini
│   ├── 📁 products/                # Her ürün için JSON dosyaları
│   └── 📁 analysis/                # Karşılaştırma sonuçları
│
├── 📁 exports/                     # Export edilen dosyalar
│
├── 📁 logs/                        # Uygulama günlük dosyaları
│   └── app.log                     # Ana log dosyası
│
├── 📁 scraper/                     # Web scraping modülleri
│   ├── __init__.py                 # Paket başlatma
│   ├── product_scraper.py          # Ana scraper sınıfı
│   ├── advanced_review_scraper_v3.py # Gelişmiş yorum çekici
│   └── (diğer scraper sürümleri)
│
├── 📁 static/                      # Statik web dosyaları
│   └── 📁 css/
│       └── style.css               # Ana stil dosyası
│
├── 📁 templates/                   # HTML şablonları
│   ├── index.html                  # Ana sayfa
│   ├── detailed_results.html       # Analiz sonuçları
│   ├── comparison_results.html     # Karşılaştırma sonuçları
│   ├── saved_products.html         # Kayıtlı ürünler
│   ├── product_detail.html         # Tek ürün detayı
│   └── error.html                  # Hata sayfası
│
├── 📁 utils/                       # Yardımcı modüller
│   ├── __init__.py                 # Paket başlatma
│   ├── config.py                   # Konfigürasyon ayarları
│   ├── data_exporter.py            # Veri export işlemleri
│   └── logger.py                   # Özelleştirilmiş logging
│
├── main.py                         # Ana uygulama dosyası (FastAPI)
├── requirements.txt                # Python bağımlılıkları
├── .env.example                    # Environment değişkenleri örneği
├── .gitignore                      # Git ignore kuralları
└── README.md                       # Bu dosya
```

## 🚀 Kurulum ve Çalıştırma

### 📋 Gereksinimler
- Python 3.8 veya üzeri
- Google Chrome tarayıcı (Selenium için)
- Gemini AI API anahtarı
- En az 4GB RAM

### 🔧 Kurulum Adımları

1. **Projeyi klonlayın**
```bash
git clone [proje-url]
cd BTK-Proje
```

2. **Sanal ortam oluşturun**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Environment dosyasını yapılandırın**
```bash
copy .env.example .env
# .env dosyasını düzenleyerek GEMINI_API_KEY ekleyin
```

5. **Uygulamayı başlatın**
```bash
python main.py
```

6. **Tarayıcıda açın**
```
http://127.0.0.1:8000
```

### 🔑 API Anahtarı Alma

1. [Google AI Studio](https://makersuite.google.com/app/apikey) adresine gidin
2. Google hesabınızla giriş yapın
3. "Create API Key" butonuna tıklayın
4. Oluşturulan anahtarı `.env` dosyasına ekleyin:
```
GEMINI_API_KEY=your_api_key_here
```

## 🖥️ Kullanım Rehberi

### 1. 📝 Tekli Ürün Analizi
- Ana sayfada ürün URL'sini girin
- "Analiz Et" butonuna tıklayın
- Detaylı analiz sonuçlarını görüntüleyin

### 2. 🔄 Çoklu Ürün Karşılaştırması
- Her satıra bir ürün URL'si girin
- "Karşılaştır" seçeneğini işaretleyin
- AI destekli karşılaştırma sonuçlarını inceleyin

### 3. 💾 Veri Yönetimi
- "Kayıtlı Ürünler" sayfasından geçmiş analizleri görün
- İstediğiniz ürünleri seçerek karşılaştırın
- JSON veya CSV formatında export edin

### 4. 📊 Sonuç Analizi
- **Genel Skor**: 100 üzerinden toplam değerlendirme
- **AI Önerisi**: Gemini AI'ın satın alma önerisi (%)
- **Duygu Analizi**: Kullanıcı yorumlarının dağılımı
- **Özellik Listesi**: AI tarafından çıkarılan ürün özellikleri

## 🛠️ Teknik Detaylar

### 🏛️ Mimari Yapı

**Backend (FastAPI)**
- **Asenkron İşleme**: Yoğun işlemler için async/await kullanımı
- **RESTful API**: Modern API tasarım prensipleri
- **Middleware**: CORS, güvenlik ve logging middleware'leri
- **Error Handling**: Kapsamlı hata yönetimi

**Frontend (HTML/CSS/JS)**
- **Jinja2 Templates**: Server-side rendering
- **Bootstrap 5**: Responsive UI framework
- **Vanilla JavaScript**: Modern JS özellikleri
- **AJAX**: Asenkron veri aktarımı

**AI/ML Stack**
- **Google Gemini**: Doğal dil işleme ve analiz
- **TextBlob**: Duygu analizi desteği
- **JSON Schema**: Yapılandırılmış AI çıktıları

**Data Storage**
- **JSON Files**: Esnek veri saklama
- **Pandas**: Veri işleme ve analiz
- **CSV Export**: Excel uyumlu veri aktarımı

### 🔧 Ana Sınıflar ve Metodlar

#### ProductScraper
```python
class ProductScraper:
    async def scrape_product(url, max_reviews=100)
    # Ürün bilgilerini ve yorumları çeker
```

#### ProductDetailedAnalyzer  
```python
class ProductDetailedAnalyzer:
    async def analyze_single_product(product_data)
    # Tek ürün için detaylı AI analizi
    
    async def compare_products(product_ids)
    # Çoklu ürün karşılaştırması
```

#### DataExporter
```python
class DataExporter:
    def export_single_product_json(analysis)
    def export_single_product_csv(analysis)
    async def export_all_products_csv(products)
```

### 📡 API Endpoints

- `GET /` - Ana sayfa
- `POST /analyze_detailed` - Detaylı ürün analizi
- `GET /saved_products` - Kayıtlı ürünler listesi
- `GET /product/{product_id}` - Tek ürün detayı
- `POST /compare_saved` - Kayıtlı ürün karşılaştırması
- `POST /api/export/product/{product_id}/{format}` - Ürün export
- `GET /api/status` - Sistem durumu

## 🔍 Algoritma Detayları

### 🤖 AI Analiz Süreci
1. **Veri Ön İşleme**: Ürün bilgilerinin temizlenmesi ve yapılandırılması
2. **Gemini AI Çağrısı**: Yapılandırılmış prompt ile AI analizi
3. **JSON Parsing**: AI çıktısının yapılandırılmış veriye dönüştürülmesi
4. **Doğrulama**: Sonuçların tutarlılık kontrolü
5. **Puanlama**: Çok kriterli skorlama sistemi

### 📊 Karşılaştırma Skoru Hesaplama
```python
# Skorlama kriterleri ve ağırlıkları
rating_score = (rating_value / 5.0) * 40  # %40
ai_score = (ai_recommendation / 100) * 30  # %30  
quality_score = (review_quality / 5.0) * 20  # %20
sentiment_score = (positive_percentage / 100) * 10  # %10
```

### 🎯 Duygu Analizi
- **Pozitif**: Olumlu yorumlar (😊)
- **Nötr**: Tarafsız yorumlar (😐)  
- **Negatif**: Olumsuz yorumlar (😞)

## 🚀 Performans Optimizasyonları

### ⚡ Hız İyileştirmeleri
- **Async/Await**: Paralel veri işleme
- **Connection Pooling**: Veritabanı bağlantı havuzu
- **Caching**: Sık kullanılan verilerin önbelleklenmesi
- **Lazy Loading**: İhtiyaç anında veri yükleme

### 🛡️ Güvenlik Önlemleri
- **Rate Limiting**: API çağrı sınırlaması
- **Input Validation**: Giriş verisi doğrulama
- **Error Sanitization**: Güvenli hata mesajları
- **Environment Variables**: API anahtarları güvenli saklama

### 📈 Ölçeklenebilirlik
- **Modüler Yapı**: Bağımsız geliştirilebilir modüller
- **Plugin Architecture**: Yeni scraper'lar kolay ekleme
- **Configuration Management**: Merkezi ayar yönetimi
- **Logging**: Detaylı sistem izleme

## 🔧 Gelişmiş Konfigürasyon

### Environment Değişkenleri
```bash
# .env dosyası
GEMINI_API_KEY=your_gemini_key
LOG_LEVEL=INFO
MAX_CONCURRENT_REQUESTS=5
SCRAPING_DELAY=2
CACHE_TIMEOUT=3600
```

### Scraping Ayarları
```python
# config.py
SCRAPING_CONFIG = {
    'max_reviews_per_product': 100,
    'request_timeout': 30,
    'retry_attempts': 3,
    'user_agents': [...]
}
```

## 🐛 Sorun Giderme

### Yaygın Hatalar ve Çözümleri

**1. Gemini API Hatası**
```
Çözüm: API anahtarının doğru olduğunu kontrol edin
Konum: .env dosyası
```

**2. Chrome Driver Hatası**
```
Çözüm: Chrome'un güncel olduğunu kontrol edin
Alternatif: Firefox driver kullanabilirsiniz
```

**3. Scraping Timeout**
```
Çözüm: İnternet bağlantınızı kontrol edin
Ayar: config.py'de timeout süresini artırın
```

**4. Memory Hatası**
```
Çözüm: Aynı anda az ürün analiz edin
Ayar: max_concurrent_requests değerini azaltın
```

### Log Dosyaları
```bash
# Ana log dosyası
logs/app.log

# Hata ayıklama için
tail -f logs/app.log
```

## 📈 Gelecek Güncellemeler

### v2.1 (Planlanıyor)
- [ ] Veritabanı desteği (PostgreSQL)
- [ ] Kullanıcı hesapları ve favoriler
- [ ] Email bildirimleri
- [ ] Fiyat takip sistemi

### v2.2 (Planlanıyor)  
- [ ] Mobil uygulama desteği
- [ ] API rate limiting
- [ ] Çoklu dil desteği
- [ ] Gelişmiş filtreleme

### v3.0 (Uzun Vadeli)
- [ ] Makine öğrenmesi modelleri
- [ ] Blockchain entegrasyonu
- [ ] IoT cihaz desteği
- [ ] AR/VR deneyimleri

## 🤝 Katkıda Bulunma

### Geliştirici Kılavuzu
1. **Fork** edin ve **clone** yapın
2. **Feature branch** oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi **commit** edin (`git commit -m 'Add amazing feature'`)
4. Branch'inizi **push** edin (`git push origin feature/amazing-feature`)
5. **Pull Request** oluşturun

### Kod Standartları
- **PEP 8**: Python kod style guide
- **Type Hints**: Tür belirtmeleri kullanın
- **Docstrings**: Fonksiyon dokümantasyonu
- **Unit Tests**: Test yazma zorunludur

## 📄 Lisans

Bu proje **MIT Lisansı** altında lisanslanmıştır. Detaylar için `LICENSE` dosyasını inceleyebilirsiniz.

## 👥 Takım - Trivox

**BTK Yarışması Trivox Takımı:**

### 👨‍💻 Serhatcan Ünal
- **Rol**: Proje Lideri & Backend Geliştirici
- **Uzmanlık**: FastAPI, AI Entegrasyonu, Sistem Mimarisi
- **Katkılar**: Ana uygulama geliştirme, AI analiz sistemi, API tasarımı

### 👩‍💻 Elif Zeynep Tosun  
- **Rol**: AI Uzmanı & Frontend Geliştirici
- **Uzmanlık**: Gemini AI, Duygu Analizi, UI/UX Tasarım
- **Katkılar**: AI algoritmaları, kullanıcı arayüzü, analiz sonuçları görselleştirme

### 👩‍💻 Meryem Gençali
- **Rol**: Web Scraping Uzmanı & UI/UX Tasarımcısı
- **Uzmanlık**: Selenium, Data Mining, Web Tasarım
- **Katkılar**: Veri çekme sistemleri, scraping optimizasyonu, responsive tasarım

##  Teşekkürler

- **Google AI**: Gemini API desteği için
- **Selenium Team**: Web scraping altyapısı için
- **FastAPI**: Modern web framework için
- **Bootstrap**: UI komponentleri için

---

**🎉 BTK Yarışması 2025 - Trivox Takımı** 

*Bu proje, Serhatcan Ünal, Elif Zeynep Tosun ve Meryem Gençali tarafından BTK Yarışması için geliştirilmiştir. Modern AI teknolojilerini e-ticaret alanında kullanarak kullanıcılara değer katmayı amaçlamaktadır.*

**Takım Trivox - "Teknoloji ile Değer Yaratan Çözümler"**
