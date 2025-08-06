"""
Data Export Modülü
Analiz sonuçlarını JSON, CSV ve Excel formatlarında export eder
"""

import json
import pandas as pd
import logging
from datetime import datetime
from typing import Dict, Any, List
from pathlib import Path

logger = logging.getLogger(__name__)


class DataExporter:
    """Veri export işlemleri"""
    
    def __init__(self):
        self.export_dir = Path("exports")
        self.export_dir.mkdir(exist_ok=True)
        
    def export_to_json(self, data: Dict[str, Any], filename: str = None) -> str:
        """JSON formatında export et"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"analiz_sonuclari_{timestamp}.json"
            
            filepath = self.export_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            
            logger.info(f"JSON export tamamlandı: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"JSON export hatası: {e}")
            raise e
    
    def export_to_csv(self, data: Dict[str, Any], filename: str = None) -> str:
        """CSV formatında export et"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"analiz_sonuclari_{timestamp}.csv"
            
            filepath = self.export_dir / filename
            
            # Ana ürün bilgilerini CSV'ye dönüştür
            rows = []
            
            # Ürün bilgileri
            for product in data.get('products', []):
                base_row = {
                    'urun_adi': product.get('title', ''),
                    'fiyat': product.get('price', ''),
                    'rating': product.get('rating', ''),
                    'platform': product.get('platform', ''),
                    'url': product.get('url', ''),
                    'yorum_sayisi': len(product.get('reviews', [])),
                    'ortalama_yorum_puani': self._calculate_avg_rating(product.get('reviews', []))
                }
                
                # Yorumları ayrı satırlar olarak ekle
                reviews = product.get('reviews', [])
                if reviews:
                    for review in reviews:
                        row = base_row.copy()
                        row.update({
                            'yorum_metni': review.get('review', ''),
                            'yorum_puani': review.get('rating', ''),
                            'yorum_yazari': review.get('author', ''),
                            'yorum_tarihi': review.get('date', ''),
                            'yorum_kaynagi': review.get('source', '')
                        })
                        rows.append(row)
                else:
                    rows.append(base_row)
            
            # DataFrame oluştur ve kaydet
            df = pd.DataFrame(rows)
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"CSV export tamamlandı: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"CSV export hatası: {e}")
            raise e
    
    def export_to_excel(self, data: Dict[str, Any], filename: str = None) -> str:
        """Excel formatında export et"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"analiz_sonuclari_{timestamp}.xlsx"
            
            filepath = self.export_dir / filename
            
            with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
                # Ürün özeti sayfası
                product_summary = []
                for product in data.get('products', []):
                    product_summary.append({
                        'Ürün Adı': product.get('title', ''),
                        'Fiyat': product.get('price', ''),
                        'Rating': product.get('rating', ''),
                        'Platform': product.get('platform', ''),
                        'Yorum Sayısı': len(product.get('reviews', [])),
                        'Ortalama Yorum Puanı': self._calculate_avg_rating(product.get('reviews', [])),
                        'URL': product.get('url', '')
                    })
                
                df_products = pd.DataFrame(product_summary)
                df_products.to_excel(writer, sheet_name='Ürün Özeti', index=False)
                
                # Yorumlar sayfası
                all_reviews = []
                for product in data.get('products', []):
                    for review in product.get('reviews', []):
                        all_reviews.append({
                            'Ürün': product.get('title', ''),
                            'Platform': product.get('platform', ''),
                            'Yorum': review.get('review', ''),
                            'Puan': review.get('rating', ''),
                            'Yazar': review.get('author', ''),
                            'Tarih': review.get('date', ''),
                            'Kaynak': review.get('source', '')
                        })
                
                if all_reviews:
                    df_reviews = pd.DataFrame(all_reviews)
                    df_reviews.to_excel(writer, sheet_name='Tüm Yorumlar', index=False)
                
                # AI Analizi sayfası
                ai_analysis = data.get('analysis', {})
                if ai_analysis:
                    analysis_data = []
                    
                    # Karşılaştırma analizi
                    comparison = ai_analysis.get('comparison_analysis', {})
                    if comparison:
                        analysis_data.append(['Karşılaştırma Analizi', ''])
                        analysis_data.append(['En İyi Değer Ürün', comparison.get('best_value_product', '')])
                        analysis_data.append(['En Yüksek Puanlı', comparison.get('highest_rated_product', '')])
                        analysis_data.append(['En Çok Yorumlanan', comparison.get('most_reviewed_product', '')])
                        analysis_data.append(['', ''])
                    
                    # Satış önerileri
                    sales_rec = ai_analysis.get('sales_recommendations', {})
                    if sales_rec:
                        analysis_data.append(['Satış Önerileri', ''])
                        for category, recommendations in sales_rec.items():
                            if isinstance(recommendations, list):
                                analysis_data.append([category.replace('_', ' ').title(), '\n'.join(recommendations)])
                            else:
                                analysis_data.append([category.replace('_', ' ').title(), str(recommendations)])
                    
                    if analysis_data:
                        df_analysis = pd.DataFrame(analysis_data, columns=['Kategori', 'Detay'])
                        df_analysis.to_excel(writer, sheet_name='AI Analizi', index=False)
            
            logger.info(f"Excel export tamamlandı: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Excel export hatası: {e}")
            raise e
    
    def _calculate_avg_rating(self, reviews: List[Dict]) -> float:
        """Ortalama rating hesapla"""
        if not reviews:
            return 0.0
        
        total_rating = 0
        valid_ratings = 0
        
        for review in reviews:
            try:
                rating = float(review.get('rating', 0))
                if rating > 0:
                    total_rating += rating
                    valid_ratings += 1
            except (ValueError, TypeError):
                continue
        
        return round(total_rating / valid_ratings, 2) if valid_ratings > 0 else 0.0
    
    def export_all_formats(self, data: Dict[str, Any], base_filename: str = None) -> Dict[str, str]:
        """Tüm formatlarda export et"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            base_name = base_filename or f"analiz_{timestamp}"
            
            results = {}
            
            # JSON export
            json_file = self.export_to_json(data, f"{base_name}.json")
            results['json'] = json_file
            
            # CSV export
            csv_file = self.export_to_csv(data, f"{base_name}.csv")
            results['csv'] = csv_file
            
            # Excel export
            excel_file = self.export_to_excel(data, f"{base_name}.xlsx")
            results['excel'] = excel_file
            
            logger.info(f"Tüm formatlar export edildi: {results}")
            return results
            
        except Exception as e:
            logger.error(f"Çoklu export hatası: {e}")
            raise e

    def export_single_product_csv(self, product_analysis: Dict[str, Any], filename: str = None) -> str:
        """Tek bir ürün analizini CSV formatında export et"""
        try:
            if not filename:
                product_id = product_analysis.get('product_id', 'unknown')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"urun_analizi_{product_id}_{timestamp}.csv"
            
            filepath = self.export_dir / filename
            
            # CSV için düz veri oluştur
            csv_data = self._flatten_product_analysis(product_analysis)
            
            df = pd.DataFrame([csv_data])
            df.to_csv(filepath, index=False, encoding='utf-8-sig')
            
            logger.info(f"Ürün CSV export tamamlandı: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Ürün CSV export hatası: {e}")
            raise e
    
    def export_single_product_json(self, product_analysis: Dict[str, Any], filename: str = None) -> str:
        """Tek bir ürün analizini JSON formatında export et"""
        try:
            if not filename:
                product_id = product_analysis.get('product_id', 'unknown')
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"urun_analizi_{product_id}_{timestamp}.json"
            
            filepath = self.export_dir / filename
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(product_analysis, f, ensure_ascii=False, indent=2)
            
            logger.info(f"Ürün JSON export tamamlandı: {filepath}")
            return str(filepath)
            
        except Exception as e:
            logger.error(f"Ürün JSON export hatası: {e}")
            raise e
    
    def _flatten_product_analysis(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Ürün analizini CSV için düzleştir"""
        try:
            basic_info = analysis.get('basic_info', {})
            review_analysis = analysis.get('review_analysis', {})
            price_analysis = analysis.get('price_analysis', {})
            rating_analysis = analysis.get('rating_analysis', {})
            ai_analysis = analysis.get('ai_analysis', {})
            
            return {
                'product_id': analysis.get('product_id', ''),
                'timestamp': analysis.get('timestamp', ''),
                'url': analysis.get('url', ''),
                'domain': analysis.get('domain', ''),
                'title': basic_info.get('title', ''),
                'brand': basic_info.get('brand', ''),
                'model': basic_info.get('model', ''),
                'price_text': price_analysis.get('original_text', ''),
                'price_value': price_analysis.get('numeric_value', ''),
                'price_category': price_analysis.get('category', ''),
                'rating_text': rating_analysis.get('original_text', ''),
                'rating_value': rating_analysis.get('numeric_value', ''),
                'rating_category': rating_analysis.get('category', ''),
                'total_reviews': review_analysis.get('total_reviews', 0),
                'positive_sentiment': review_analysis.get('sentiment_percentages', {}).get('positive', 0),
                'negative_sentiment': review_analysis.get('sentiment_percentages', {}).get('negative', 0),
                'review_quality_score': review_analysis.get('review_quality_score', 0),
                'ai_category': ai_analysis.get('category', ''),
                'ai_recommendation': ai_analysis.get('purchase_recommendation', 0),
                'ai_strengths': ' | '.join(ai_analysis.get('strengths', [])),
                'ai_weaknesses': ' | '.join(ai_analysis.get('weaknesses', [])),
                'color_analysis': ai_analysis.get('color_analysis', ''),
                'price_competitiveness': ai_analysis.get('price_competitiveness', ''),
                'user_satisfaction': ai_analysis.get('user_satisfaction', ''),
                'sales_potential': ai_analysis.get('sales_potential', '')
            }
            
        except Exception as e:
            logger.error(f"Düzleştirme hatası: {e}")
            return {'error': str(e)}
