# 🤝 Katkıda Bulunma Rehberi

## BTK Yarışması 2025 - Trivox Takımı

Bu proje **BTK Yarışması 2025** için **Trivox takımı** tarafından geliştirilmiştir. 

### 👥 Takım Üyeleri
- **Serhatcan Ünal** - Proje Lideri & Backend Geliştirici
- **Elif Zeynep Tosun** - AI Uzmanı & Frontend Geliştirici  
- **Meryem Gençali** - Web Scraping Uzmanı & UI/UX Tasarımcısı

## 🚀 Geliştirme Ortamı Kurulumu

### Ön Gereksinimler
- Python 3.8+
- Git
- Google Chrome
- Gemini AI API Key

### Kurulum Adımları

1. **Repository'yi fork edin ve klonlayın**
```bash
git clone https://github.com/serhatcanunal1/btk_urun_analiz.git
cd btk_urun_analiz
```

2. **Sanal ortam oluşturun**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. **Bağımlılıkları yükleyin**
```bash
pip install -r requirements.txt
```

4. **Environment dosyasını yapılandırın**
```bash
copy .env.example .env
# .env dosyasını düzenleyerek gerekli anahtarları ekleyin
```

## 📁 Proje Yapısı

```
btk_urun_analiz/
├── analyzer/          # AI analiz modülleri
├── scraper/           # Web scraping modülleri  
├── templates/         # HTML şablonları
├── static/            # CSS, JS dosyaları
├── utils/             # Yardımcı modüller
├── data/              # Veri depolama
├── exports/           # Export dosyaları
├── logs/              # Log dosyaları
└── main.py            # Ana uygulama
```

## 🔧 Kod Standartları

### Python Kod Stili
- **PEP 8** standartlarını takip edin
- **Type hints** kullanın
- **Docstring**'leri ekleyin
- **Async/await** pattern'ini tercih edin

### Commit Mesajları
```
🏆 [BTK] Yeni özellik açıklaması
🐛 [FIX] Hata düzeltmesi açıklaması  
🔧 [CONFIG] Konfigürasyon değişikliği
📚 [DOCS] Dokümantasyon güncellemesi
🎨 [UI] Arayüz iyileştirmesi
```

### Branch Yapısı
```
main              # Ana production branch
develop           # Geliştirme branch'i
feature/xxx       # Yeni özellik branch'leri
bugfix/xxx        # Hata düzeltme branch'leri
```

## 🧪 Test Etme

### Manuel Test
```bash
python main.py
# http://127.0.0.1:8000 adresinde test edin
```

### API Test
```bash
# Sistem durumu testi
curl http://127.0.0.1:8000/api/status

# Hızlı test
curl http://127.0.0.1:8000/api/quick_test
```

## 📊 Pull Request Süreci

1. **Fork** projeyi kendi hesabınıza
2. **Branch** oluşturun: `git checkout -b feature/yeni-ozellik`
3. **Commit** yapın: `git commit -m '🏆 [BTK] Yeni özellik eklendi'`
4. **Push** edin: `git push origin feature/yeni-ozellik`
5. **Pull Request** oluşturun

### PR Kontrol Listesi
- [ ] Kod PEP 8 standartlarına uygun
- [ ] Type hints eklenmiş
- [ ] Docstring'ler yazılmış
- [ ] Test edilmiş ve çalışıyor
- [ ] Dokümantasyon güncellenmiş

## 🐛 Issue Raporlama

Issue açarken lütfen şunları belirtin:

### Bug Report Template
```
**🐛 Hata Açıklaması**
Kısa ve net hata açıklaması

**🔄 Tekrarlama Adımları**
1. Şunu yap
2. Bunu tıkla
3. Hatayı gör

**💻 Sistem Bilgisi**
- OS: [Windows/Linux/Mac]
- Python: [versiyon]
- Browser: [Chrome/Firefox/etc]

**📝 Ek Bilgiler**
Log dosyaları, ekran görüntüsü vs.
```

### Feature Request Template
```
**✨ Özellik Önerisi**
Önerilen özelliğin açıklaması

**🎯 Kullanım Senaryosu**
Bu özellik neden gerekli?

**💡 Önerilen Çözüm**
Nasıl implement edilebilir?
```

## 📚 Geliştirme Kaynakları

### Kullanılan Teknolojiler
- **FastAPI**: Web framework
- **Google Gemini AI**: AI analizi
- **Selenium**: Web scraping
- **Bootstrap 5**: Frontend framework
- **Jinja2**: Template engine

### Faydalı Linkler
- [FastAPI Dokümantasyonu](https://fastapi.tiangolo.com/)
- [Gemini AI Rehberi](https://ai.google.dev/docs)
- [Selenium Dokümantasyonu](https://selenium-python.readthedocs.io/)

## 📞 İletişim

**Trivox Takımı ile iletişime geçin:**
- **Proje Lideri**: Serhatcan Ünal
- **AI Uzmanı**: Elif Zeynep Tosun
- **Web Scraping Uzmanı**: Meryem Gençali

---

**🎉 BTK Yarışması 2025 - Trivox Takımı**

*"Teknoloji ile Değer Yaratan Çözümler"*
