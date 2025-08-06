"""
Ürün Analiz Sistemi v2 - Gelişmiş Ana Uygulama
Her ürünü detaylıca analiz eden ve karşılaştıran sistem
"""

import uvicorn
import os
import logging
import asyncio
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from dotenv import load_dotenv

from scraper.product_scraper import ProductScraper
from analyzer.product_detailed_analyzer import ProductDetailedAnalyzer
from utils.data_exporter import DataExporter

# Environment yükle
load_dotenv()

# Logging ayarları
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Ürün Analiz Sistemi v2",
    description="Detaylı ürün analizi ve AI destekli karşılaştırma sistemi",
    version="2.0.0"
)

# Templates ve static files
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# API anahtarı kontrolü
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if not GEMINI_API_KEY:
    logger.error("GEMINI_API_KEY environment variable bulunamadı!")
    GEMINI_API_KEY = "demo_key"  # Demo için

# Global nesneler
scraper = ProductScraper()
detailed_analyzer = ProductDetailedAnalyzer(GEMINI_API_KEY)
data_exporter = DataExporter()


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Ana sayfa"""
    try:
        # Kaydedilmiş ürün sayısını al
        saved_products = detailed_analyzer.get_all_product_ids()
        saved_count = len(saved_products)
        
        return templates.TemplateResponse("index_v2.html", {
            "request": request,
            "saved_products_count": saved_count,
            "recent_products": saved_products[-5:] if saved_products else []
        })
    except Exception as e:
        logger.error(f"Ana sayfa hatası: {e}")
        return templates.TemplateResponse("index_v2.html", {
            "request": request,
            "saved_products_count": 0,
            "recent_products": []
        })


@app.post("/analyze_detailed")
async def analyze_products_detailed(
    request: Request,
    product_urls: str = Form(...),
    max_reviews: int = Form(100),
    show_reviews: bool = Form(False)
):
    """Detaylı ürün analizi - Her ürünü ayrı ayrı analiz et"""
    try:
        # URL'leri parse et
        urls = [url.strip() for url in product_urls.split('\n') if url.strip()]
        
        if not urls:
            raise HTTPException(status_code=400, detail="En az bir URL girmelisiniz")
        
        logger.info(f"=== DETAYLI ANALİZ BAŞLADI ===")
        logger.info(f"Toplam URL sayısı: {len(urls)}")
        logger.info(f"Maksimum yorum sayısı: {max_reviews}")
        logger.info(f"Yorumları göster: {show_reviews}")
        
        # Her URL'yi ayrı ayrı işle
        all_results = []
        failed_urls = []
        
        for i, url in enumerate(urls, 1):
            logger.info(f"\\n--- ÜRÜN {i}/{len(urls)} ANALİZİ ---")
            logger.info(f"URL: {url}")
            
            try:
                # 1. Ürünü scrape et
                logger.info("1. Ürün scraping başlıyor...")
                scraped_data = await scraper.scrape_product(url, max_reviews=max_reviews)
                
                if not scraped_data.get('success'):
                    logger.error(f"Scraping başarısız: {scraped_data.get('error', 'Bilinmeyen hata')}")
                    failed_urls.append(url)
                    continue
                
                logger.info(f"Scraping başarılı: {scraped_data.get('title', '')[:50]}...")
                logger.info(f"Yorum sayısı: {len(scraped_data.get('reviews', []))}")
                
                # 2. Detaylı analiz et
                logger.info("2. Detaylı AI analizi başlıyor...")
                detailed_analysis = await detailed_analyzer.analyze_single_product(scraped_data)
                
                if detailed_analysis.get('error'):
                    logger.error(f"Analiz hatası: {detailed_analysis['error']}")
                    failed_urls.append(url)
                    continue
                
                logger.info(f"Analiz başarılı - Ürün ID: {detailed_analysis.get('product_id')}")
                all_results.append(detailed_analysis)
                
            except Exception as e:
                logger.error(f"Ürün {i} işleme hatası: {e}")
                failed_urls.append(url)
                continue
        
        logger.info(f"\\n=== ANALİZ TAMAMLANDI ===")
        logger.info(f"Başarılı: {len(all_results)} ürün")
        logger.info(f"Başarısız: {len(failed_urls)} ürün")
        
        if not all_results:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Hiçbir ürün başarıyla analiz edilemedi",
                "failed_urls": failed_urls
            })
        
        # 3. Karşılaştırma yap (2+ ürün varsa)
        comparison_result = None
        if len(all_results) > 1:
            logger.info("3. Ürün karşılaştırması başlıyor...")
            product_ids = [result['product_id'] for result in all_results]
            comparison_result = await detailed_analyzer.compare_products(product_ids)
            logger.info("Karşılaştırma tamamlandı")
        
        # Sonuç sayfasını göster
        return templates.TemplateResponse("detailed_results.html", {
            "request": request,
            "products": all_results,
            "comparison": comparison_result,
            "total_products": len(all_results),
            "failed_count": len(failed_urls),
            "failed_urls": failed_urls,
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "show_reviews": show_reviews,
            "max_reviews_used": max_reviews
        })
        
    except Exception as e:
        logger.error(f"Genel analiz hatası: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Analiz hatası: {str(e)}"
        })


@app.get("/saved_products")
async def get_saved_products(request: Request):
    """Kaydedilmiş ürünleri listele"""
    try:
        product_ids = detailed_analyzer.get_all_product_ids()
        products = []
        
        for product_id in product_ids[-20:]:  # Son 20 ürün
            analysis = detailed_analyzer.get_product_analysis(product_id)
            if analysis:
                products.append({
                    'id': product_id,
                    'title': analysis.get('basic_info', {}).get('title', 'Başlık yok'),
                    'domain': analysis.get('domain', 'Bilinmeyen'),
                    'timestamp': analysis.get('timestamp', ''),
                    'price': analysis.get('price_analysis', {}).get('original_text', 'Fiyat yok'),
                    'rating': analysis.get('rating_analysis', {}).get('original_text', 'Rating yok')
                })
        
        return templates.TemplateResponse("saved_products.html", {
            "request": request,
            "products": products,
            "total_count": len(product_ids)
        })
        
    except Exception as e:
        logger.error(f"Kaydedilmiş ürünler hatası: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Ürünler yüklenemedi: {str(e)}"
        })


@app.get("/product/{product_id}")
async def get_product_detail(request: Request, product_id: str):
    """Tek ürün detayını göster"""
    try:
        analysis = detailed_analyzer.get_product_analysis(product_id)
        
        if not analysis:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        
        return templates.TemplateResponse("product_detail.html", {
            "request": request,
            "product": analysis
        })
        
    except Exception as e:
        logger.error(f"Ürün detayı hatası: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Ürün yüklenemedi: {str(e)}"
        })


@app.post("/compare_saved")
async def compare_saved_products(
    request: Request,
    selected_products: str = Form(...)
):
    """Kaydedilmiş ürünleri karşılaştır"""
    try:
        product_ids = [pid.strip() for pid in selected_products.split(',') if pid.strip()]
        
        if len(product_ids) < 2:
            raise HTTPException(status_code=400, detail="En az 2 ürün seçmelisiniz")
        
        logger.info(f"Kaydedilmiş ürün karşılaştırması: {len(product_ids)} ürün")
        
        comparison_result = await detailed_analyzer.compare_products(product_ids)
        
        if comparison_result.get('error'):
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": comparison_result['error']
            })
        
        return templates.TemplateResponse("comparison_results.html", {
            "request": request,
            "comparison": comparison_result
        })
        
    except Exception as e:
        logger.error(f"Karşılaştırma hatası: {e}")
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": f"Karşılaştırma hatası: {str(e)}"
        })


# Export API'leri
@app.post("/api/export/product/{product_id}/json")
async def export_product_json(product_id: str):
    """Tek ürünü JSON olarak export et"""
    try:
        analysis = detailed_analyzer.get_product_analysis(product_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        
        filename = data_exporter.export_single_product_json(analysis)
        return JSONResponse({
            "success": True,
            "message": "JSON export başarılı",
            "filename": filename,
            "product_id": product_id
        })
        
    except Exception as e:
        logger.error(f"JSON export hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export/product/{product_id}/csv")
async def export_product_csv(product_id: str):
    """Tek ürünü CSV olarak export et"""
    try:
        analysis = detailed_analyzer.get_product_analysis(product_id)
        if not analysis:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı")
        
        filename = data_exporter.export_single_product_csv(analysis)
        return JSONResponse({
            "success": True,
            "message": "CSV export başarılı",
            "filename": filename,
            "product_id": product_id
        })
        
    except Exception as e:
        logger.error(f"CSV export hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/export/all_products/csv")
async def export_all_products_csv():
    """Tüm ürünleri CSV olarak export et"""
    try:
        product_ids = detailed_analyzer.get_all_product_ids()
        
        if not product_ids:
            raise HTTPException(status_code=404, detail="Kaydedilmiş ürün bulunamadı")
        
        products = []
        for product_id in product_ids:
            analysis = detailed_analyzer.get_product_analysis(product_id)
            if analysis:
                products.append(analysis)
        
        filename = await data_exporter.export_all_products_csv(products)
        return JSONResponse({
            "success": True,
            "message": f"{len(products)} ürün CSV olarak export edildi",
            "filename": filename,
            "download_url": f"/api/download/{filename}"
        })
        
    except Exception as e:
        logger.error(f"Toplu CSV export hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/download/{filename}")
async def download_file(filename: str):
    """Export edilen dosyayı indir"""
    try:
        file_path = Path("exports") / filename
        
        if not file_path.exists():
            raise HTTPException(status_code=404, detail="Dosya bulunamadı")
        
        return FileResponse(
            path=file_path,
            filename=filename,
            media_type='application/octet-stream'
        )
        
    except Exception as e:
        logger.error(f"Download hatası: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# API durumu
@app.get("/api/status")
async def api_status():
    """API durumu"""
    try:
        saved_count = len(detailed_analyzer.get_all_product_ids())
        
        return JSONResponse({
            "status": "active",
            "version": "2.0.0",
            "saved_products": saved_count,
            "features": [
                "Detaylı ürün analizi",
                "AI destekli karşılaştırma",
                "Duygu analizi",
                "Çoklu format export",
                "Ürün kaydetme"
            ]
        })
        
    except Exception as e:
        return JSONResponse({
            "status": "error",
            "error": str(e)
        })


@app.post("/api/test_analysis")
async def test_single_product_analysis():
    """Tek ürün test analizi - Hızlı test için"""
    try:
        # Test verisi oluştur
        test_product = {
            'success': True,
            'title': 'Test Xiaomi Redmi 13 8GB RAM 256GB Mavi Cep Telefonu',
            'domain': 'test.com',
            'url': 'https://test.com/product',
            'price': '3.299,00 TL',
            'rating': '4.5 yıldız',
            'reviews': [
                {"text": "Çok güzel telefon, hızlı çalışıyor", "rating": "5"},
                {"text": "Fiyat performans açısından ideal", "rating": "4"},
                {"text": "Kamera kalitesi iyi, batarya uzun gidiyor", "rating": "5"},
                {"text": "Tavsiye ederim, kaliteli ürün", "rating": "4"}
            ],
            'images': [],
            'review_count': 4
        }
        
        logger.info("Test ürün analizi başlatılıyor...")
        
        # Detaylı analiz et
        detailed_analysis = await detailed_analyzer.analyze_single_product(test_product)
        
        logger.info(f"Test analiz tamamlandı: {detailed_analysis.get('product_id')}")
        
        return JSONResponse({
            "success": True,
            "message": "Test analizi başarılı",
            "product_id": detailed_analysis.get('product_id'),
            "analysis_summary": {
                "ai_recommendation": detailed_analysis.get('ai_analysis', {}).get('purchase_recommendation', 0),
                "category": detailed_analysis.get('ai_analysis', {}).get('category', 'Unknown'),
                "sentiment_positive": detailed_analysis.get('review_analysis', {}).get('sentiment_percentages', {}).get('positive', 0),
                "price_category": detailed_analysis.get('price_analysis', {}).get('category', 'Unknown')
            }
        })
        
    except Exception as e:
        logger.error(f"Test analizi hatası: {e}")
        return JSONResponse({
            "success": False,
            "error": str(e)
        })


@app.get("/api/quick_test")
async def quick_test():
    """Sistem hızlı test"""
    try:
        # 1. Veri kaydetme testi
        test_data = {"test": "data", "timestamp": datetime.now().isoformat()}
        
        # 2. AI bağlantı testi (kısa timeout ile)
        ai_test = "OK"
        try:
            import google.generativeai as genai
            genai.configure(api_key=GEMINI_API_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            response = await asyncio.wait_for(
                asyncio.to_thread(model.generate_content, "Test: 1+1=?"),
                timeout=10.0
            )
            if "2" in response.text:
                ai_test = "OK"
            else:
                ai_test = "Response error"
                
        except asyncio.TimeoutError:
            ai_test = "Timeout"
        except Exception as e:
            ai_test = f"Error: {str(e)[:50]}"
        
        return JSONResponse({
            "system_status": "OK",
            "ai_connection": ai_test,
            "directories": {
                "data": Path("data").exists(),
                "products": Path("data/products").exists(),
                "exports": Path("exports").exists()
            },
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        return JSONResponse({
            "system_status": "ERROR",
            "error": str(e)
        })


if __name__ == "__main__":
    # Dizinleri oluştur
    Path("logs").mkdir(exist_ok=True)
    Path("exports").mkdir(exist_ok=True)
    Path("data").mkdir(exist_ok=True)
    Path("data/products").mkdir(exist_ok=True)
    Path("data/analysis").mkdir(exist_ok=True)
    
    logger.info("🚀 Ürün Analiz Sistemi v2 başlatılıyor...")
    logger.info("✅ Detaylı analiz sistemi aktif")
    logger.info("✅ AI destekli karşılaştırma aktif")
    logger.info("✅ Çoklu format export aktif")
    
    uvicorn.run(
        "main_v2:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
