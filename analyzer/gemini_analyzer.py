"""
Gemini AI Analyzer Modülü
Ürün verilerini ve yorumları analiz eder
"""

import google.generativeai as genai
from typing import List, Dict, Any, Optional
import json
import asyncio
import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class GeminiAnalyzer:
    """Gemini AI kullanarak ürün analizi yapan sınıf"""
    
    def __init__(self, api_key: str):
        """Gemini API'yi başlat"""
        if not api_key or api_key == "your_gemini_api_key_here":
            raise ValueError("Geçerli bir Gemini API anahtarı gerekli")
        
        genai.configure(api_key=api_key)
        # Yeni model adını kullan
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    async def analyze_products(self, products_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Çoklu ürün analizi"""
        try:
            logger.info(f"Analiz başlatılıyor: {len(products_data)} ürün")
            
            # Her ürün için ayrı analiz
            product_analyses = []
            for product in products_data:
                analysis = await self._analyze_single_product(product)
                product_analyses.append(analysis)
            
            # Genel karşılaştırma analizi
            comparison_analysis = await self._compare_products(products_data)
            
            # Satış önerileri
            sales_recommendations = await self._generate_sales_recommendations(products_data, product_analyses)
            
            # Sonuçları birleştir
            final_analysis = {
                'timestamp': datetime.now().isoformat(),
                'total_products': len(products_data),
                'product_analyses': product_analyses,
                'comparison_analysis': comparison_analysis,
                'sales_recommendations': sales_recommendations,
                'summary': await self._generate_summary(products_data, product_analyses)
            }
            
            logger.info("Analiz tamamlandı")
            return final_analysis
            
        except Exception as e:
            logger.error(f"Analiz hatası: {e}")
            raise e
    
    async def _analyze_single_product(self, product: Dict[str, Any]) -> Dict[str, Any]:
        """Tek ürün analizi"""
        try:
            # Yorum analizi
            review_analysis = await self._analyze_reviews(product.get('reviews', []))
            
            # Fiyat analizi
            price_analysis = self._analyze_price(product.get('price', ''))
            
            # Rating analizi
            rating_analysis = self._analyze_rating(product.get('rating', ''))
            
            return {
                'product_title': product.get('title', 'Bilinmeyen'),
                'marketplace': product.get('domain', 'Bilinmeyen'),
                'url': product.get('url', ''),
                'review_analysis': review_analysis,
                'price_analysis': price_analysis,
                'rating_analysis': rating_analysis,
                'overall_score': self._calculate_overall_score(review_analysis, price_analysis, rating_analysis)
            }
            
        except Exception as e:
            logger.error(f"Tek ürün analiz hatası: {e}")
            return {
                'product_title': product.get('title', 'Bilinmeyen'),
                'marketplace': product.get('domain', 'Bilinmeyen'),
                'error': str(e)
            }
    
    async def _analyze_reviews(self, reviews: List[Dict[str, str]]) -> Dict[str, Any]:
        """Yorumları Gemini ile analiz et"""
        if not reviews:
            return {
                'total_reviews': 0,
                'sentiment_summary': 'Yorum bulunamadı',
                'common_themes': [],
                'pros': [],
                'cons': [],
                'sentiment_score': 0,
                'key_insights': []
            }
        
        try:
            # Yorumları tek bir string'e birleştir (daha fazla veri ile)
            reviews_text = ""
            for i, review in enumerate(reviews[:30]):  # İlk 30 yorumu analiz et
                reviews_text += f"Yorum {i+1} (Rating: {review.get('rating', 'N/A')}): {review['text']}\n\n"
            
            # Daha detaylı ve spesifik prompt
            prompt = f"""
            Aşağıdaki {len(reviews)} ürün yorumunu detaylı olarak analiz et ve e-ticaret satıcısı perspektifinden değerlendir:

            YORUMLAR:
            {reviews_text}

            Lütfen aşağıdaki JSON formatında TÜRKÇE yanıt ver. Sadece JSON formatında yanıt ver, başka hiçbir şey yazma:
            {{
                "sentiment_summary": "Genel duygu durumu özeti (çok pozitif/pozitif/nötr/negatif/çok negatif)",
                "sentiment_score": <0-10 arası sayısal skor>,
                "common_themes": [
                    "En sık bahsedilen tema 1",
                    "En sık bahsedilen tema 2", 
                    "En sık bahsedilen tema 3",
                    "En sık bahsedilen tema 4"
                ],
                "pros": [
                    "Müşterilerin en çok beğendiği özellik 1",
                    "Müşterilerin en çok beğendiği özellik 2",
                    "Müşterilerin en çok beğendiği özellik 3",
                    "Müşterilerin en çok beğendiği özellik 4",
                    "Müşterilerin en çok beğendiği özellik 5"
                ],
                "cons": [
                    "Müşterilerin en çok şikayet ettiği nokta 1",
                    "Müşterilerin en çok şikayet ettiği nokta 2",
                    "Müşterilerin en çok şikayet ettiği nokta 3",
                    "Müşterilerin en çok şikayet ettiği nokta 4"
                ],
                "key_insights": [
                    "Satıcı için önemli çıkarım 1",
                    "Satıcı için önemli çıkarım 2",
                    "Satıcı için önemli çıkarım 3",
                    "Müşteri beklentisi hakkında çıkarım 1",
                    "Ürün kalitesi hakkında çıkarım 1"
                ],
                "customer_satisfaction": "müşteri memnuniyet durumu özeti",
                "improvement_suggestions": [
                    "İyileştirme önerisi 1",
                    "İyileştirme önerisi 2",
                    "İyileştirme önerisi 3"
                ],
                "target_audience": "bu ürünü satın alan müşteri profili",
                "competitive_advantage": "rakiplerine karşı avantajları",
                "risk_factors": [
                    "Potansiyel risk faktörü 1",
                    "Potansiyel risk faktörü 2"
                ]
            }}
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            # JSON parse et
            try:
                analysis_result = json.loads(response.text.strip())
                analysis_result['total_reviews'] = len(reviews)
                
                # Skor validasyonu
                if 'sentiment_score' in analysis_result:
                    score = analysis_result['sentiment_score']
                    if not isinstance(score, (int, float)) or score < 0 or score > 10:
                        analysis_result['sentiment_score'] = 5
                
                logger.info(f"Detaylı yorum analizi tamamlandı: {len(reviews)} yorum")
                return analysis_result
                
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse hatası: {e}")
                logger.debug(f"AI response: {response.text[:500]}")
                
                # Fallback analiz
                return self._fallback_review_analysis(reviews)
                
        except Exception as e:
            logger.error(f"Yorum analiz hatası: {e}")
            return self._fallback_review_analysis(reviews)
    
    def _fallback_review_analysis(self, reviews: List[Dict[str, str]]) -> Dict[str, Any]:
        """Basit fallback yorum analizi"""
        try:
            # Basit sentiment analizi
            positive_words = ['güzel', 'iyi', 'memnun', 'kaliteli', 'harika', 'mükemmel', 'tavsiye', 'başarılı']
            negative_words = ['kötü', 'berbat', 'sorunlu', 'bozuk', 'pahalı', 'geç', 'yavaş', 'eksik']
            
            positive_count = 0
            negative_count = 0
            all_text = ""
            
            for review in reviews:
                text = review['text'].lower()
                all_text += text + " "
                
                for word in positive_words:
                    positive_count += text.count(word)
                for word in negative_words:
                    negative_count += text.count(word)
            
            # Skor hesapla
            total_sentiment = positive_count - negative_count
            sentiment_score = max(0, min(10, 5 + (total_sentiment / max(1, len(reviews)))))
            
            # Basit tema çıkarımı
            common_themes = []
            if 'kalite' in all_text:
                common_themes.append('Ürün kalitesi')
            if 'fiyat' in all_text:
                common_themes.append('Fiyat')
            if 'kargo' in all_text:
                common_themes.append('Kargo ve teslimat')
            if 'kullanım' in all_text:
                common_themes.append('Kullanım deneyimi')
            
            return {
                'total_reviews': len(reviews),
                'sentiment_summary': 'Orta düzeyde pozitif' if sentiment_score > 5 else 'Karışık',
                'sentiment_score': round(sentiment_score, 1),
                'common_themes': common_themes[:4],
                'pros': ['Kullanıcılar tarafından beğeniliyor', 'Genel olarak olumlu geri bildirimler'],
                'cons': ['Bazı kullanıcılar sorun bildirmiş', 'İyileştirme alanları mevcut'],
                'key_insights': ['Detaylı AI analizi yapılamadı', 'Basit analiz kullanıldı'],
                'customer_satisfaction': 'Orta düzeyde memnuniyet',
                'improvement_suggestions': ['Müşteri geri bildirimlerini takip edin'],
                'target_audience': 'Genel kullanıcı kitlesi',
                'competitive_advantage': 'Analiz edilemedi',
                'risk_factors': ['Detaylı analiz gerekli']
            }
            
        except Exception as e:
            logger.error(f"Fallback analiz hatası: {e}")
            return {
                'total_reviews': len(reviews),
                'sentiment_summary': 'Analiz yapılamadı',
                'sentiment_score': 5,
                'common_themes': [],
                'pros': [],
                'cons': [],
                'key_insights': [],
                'customer_satisfaction': 'Bilinmiyor',
                'improvement_suggestions': [],
                'target_audience': 'Bilinmiyor',
                'competitive_advantage': 'Bilinmiyor',
                'risk_factors': []
            }
    
    def _analyze_price(self, price_str: str) -> Dict[str, Any]:
        """Fiyat analizi"""
        try:
            # Fiyattan sayısal değeri çıkar
            import re
            price_numbers = re.findall(r'\d+[\.,]?\d*', price_str.replace('.', '').replace(',', '.'))
            
            if price_numbers:
                price_value = float(price_numbers[0])
                
                # Fiyat kategorisi belirle
                if price_value < 100:
                    category = "Düşük fiyat segmenti"
                elif price_value < 500:
                    category = "Orta fiyat segmenti"
                elif price_value < 1000:
                    category = "Yüksek fiyat segmenti"
                else:
                    category = "Premium fiyat segmenti"
                
                return {
                    'price_text': price_str,
                    'price_value': price_value,
                    'price_category': category,
                    'price_analysis': f"Bu ürün {category.lower()}'nde yer almaktadır."
                }
            else:
                return {
                    'price_text': price_str,
                    'price_value': 0,
                    'price_category': 'Fiyat belirlenemedi',
                    'price_analysis': 'Fiyat bilgisi net değil'
                }
                
        except Exception as e:
            return {
                'price_text': price_str,
                'price_value': 0,
                'price_category': 'Analiz hatası',
                'price_analysis': f'Fiyat analizi yapılamadı: {str(e)}'
            }
    
    def _analyze_rating(self, rating_str: str) -> Dict[str, Any]:
        """Rating analizi"""
        try:
            import re
            rating_numbers = re.findall(r'\d+[\.,]?\d*', rating_str)
            
            if rating_numbers:
                rating_value = float(rating_numbers[0])
                
                if rating_value >= 4.5:
                    analysis = "Mükemmel rating - Müşteri memnuniyeti çok yüksek"
                elif rating_value >= 4.0:
                    analysis = "İyi rating - Müşteri memnuniyeti yüksek"
                elif rating_value >= 3.5:
                    analysis = "Orta rating - Müşteri memnuniyeti ortalama"
                elif rating_value >= 3.0:
                    analysis = "Düşük rating - Müşteri memnuniyeti düşük"
                else:
                    analysis = "Çok düşük rating - Ciddi sorunlar var"
                
                return {
                    'rating_text': rating_str,
                    'rating_value': rating_value,
                    'rating_analysis': analysis
                }
            else:
                return {
                    'rating_text': rating_str,
                    'rating_value': 0,
                    'rating_analysis': 'Rating bilgisi bulunamadı'
                }
                
        except Exception as e:
            return {
                'rating_text': rating_str,
                'rating_value': 0,
                'rating_analysis': f'Rating analizi yapılamadı: {str(e)}'
            }
    
    def _calculate_overall_score(self, review_analysis: Dict, price_analysis: Dict, rating_analysis: Dict) -> float:
        """Genel skor hesaplama"""
        try:
            sentiment_score = review_analysis.get('sentiment_score', 0) * 0.4
            rating_score = rating_analysis.get('rating_value', 0) * 2 * 0.4  # 5'ten 10'a çevir
            price_score = 5 * 0.2  # Fiyat için sabit skor
            
            total_score = sentiment_score + rating_score + price_score
            return round(total_score, 2)
            
        except Exception:
            return 5.0
    
    async def _compare_products(self, products_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Ürünleri karşılaştır"""
        try:
            if len(products_data) < 2:
                return {
                    'comparison_summary': 'Karşılaştırma için en az 2 ürün gerekli',
                    'best_product': products_data[0] if products_data else None,
                    'price_comparison': 'Yetersiz veri'
                }
            
            # Detaylı karşılaştırma için AI kullan
            try:
                comparison_data = []
                for i, product in enumerate(products_data[:5]):  # İlk 5 ürünü karşılaştır
                    comparison_data.append({
                        'sira': i + 1,
                        'baslik': product.get('title', 'Bilinmeyen')[:100],
                        'pazaryeri': product.get('domain', 'Bilinmeyen'),
                        'fiyat': product.get('price', 'Bilinmeyen'),
                        'rating': product.get('rating', 'Bilinmeyen'),
                        'yorum_sayisi': len(product.get('reviews', []))
                    })
                
                prompt = f"""
                Aşağıdaki ürünleri detaylı olarak karşılaştır ve e-ticaret satıcısı perspektifinden analiz et:

                ÜRÜNLER:
                {json.dumps(comparison_data, ensure_ascii=False, indent=2)}

                Lütfen aşağıdaki JSON formatında yanıt ver:
                {{
                    "comparison_summary": "Genel karşılaştırma özeti",
                    "best_value_product": "En iyi value for money ürün",
                    "highest_rated_product": "En yüksek puanlı ürün", 
                    "most_reviewed_product": "En çok yorumlanan ürün",
                    "price_analysis": {{
                        "cheapest": "En ucuz ürün bilgisi",
                        "most_expensive": "En pahalı ürün bilgisi",
                        "price_range": "Fiyat aralığı analizi"
                    }},
                    "marketplace_analysis": {{
                        "best_marketplace": "En iyi pazaryeri",
                        "marketplace_comparison": "Pazaryeri karşılaştırması"
                    }},
                    "recommendations": [
                        "Satıcı için öneri 1",
                        "Satıcı için öneri 2",
                        "Satıcı için öneri 3"
                    ],
                    "competitive_insights": [
                        "Rekabet insight 1",
                        "Rekabet insight 2",
                        "Rekabet insight 3"
                    ]
                }}
                
                Sadece JSON formatında yanıt ver, başka hiçbir şey ekleme.
                """
                
                response = await asyncio.to_thread(self.model.generate_content, prompt)
                
                try:
                    ai_comparison = json.loads(response.text.strip())
                    
                    # Temel bilgileri ekle
                    ai_comparison['total_products'] = len(products_data)
                    ai_comparison['marketplaces'] = list(set([p.get('domain', 'Bilinmeyen') for p in products_data]))
                    ai_comparison['total_reviews'] = sum([len(p.get('reviews', [])) for p in products_data])
                    
                    return ai_comparison
                    
                except json.JSONDecodeError:
                    logger.warning("AI karşılaştırma JSON parse edilemedi, fallback kullanılıyor")
                    
            except Exception as e:
                logger.error(f"AI karşılaştırma hatası: {e}")
            
            # Fallback: Basit karşılaştırma
            marketplaces = list(set([p.get('domain', 'Bilinmeyen') for p in products_data]))
            total_reviews = sum([len(p.get('reviews', [])) for p in products_data])
            
            # En çok yorumlanan ürünü bul
            most_reviewed = max(products_data, key=lambda x: len(x.get('reviews', [])))
            
            # Fiyat analizi
            prices = []
            for product in products_data:
                price_text = product.get('price', '')
                numbers = re.findall(r'\d+', price_text.replace('.', '').replace(',', ''))
                if numbers:
                    try:
                        prices.append(float(numbers[0]))
                    except:
                        pass
            
            price_analysis = "Fiyat karşılaştırması yapılamadı"
            if prices:
                min_price = min(prices)
                max_price = max(prices)
                avg_price = sum(prices) / len(prices)
                price_analysis = f"En düşük: {min_price:.0f} TL, En yüksek: {max_price:.0f} TL, Ortalama: {avg_price:.0f} TL"
            
            return {
                'comparison_summary': f"{len(products_data)} ürün {len(marketplaces)} farklı pazaryerinde analiz edildi",
                'marketplaces': marketplaces,
                'total_reviews': total_reviews,
                'price_comparison': price_analysis,
                'most_reviewed_product': most_reviewed.get('title', 'Bilinmeyen')[:50],
                'marketplace_analysis': {
                    'marketplace_count': len(marketplaces),
                    'marketplaces': marketplaces
                },
                'recommendations': [
                    f"En çok yorumlanan ürün: {most_reviewed.get('title', 'Bilinmeyen')[:30]}",
                    f"Toplam {total_reviews} müşteri yorumu incelendi",
                    "Detaylı AI analizi için sistem güncellemesi gerekiyor"
                ]
            }
            
        except Exception as e:
            logger.error(f"Karşılaştırma hatası: {e}")
            return {
                'comparison_summary': f'Karşılaştırma hatası: {str(e)}',
                'error': True,
                'total_products': len(products_data),
                'marketplaces': list(set([p.get('domain', 'Bilinmeyen') for p in products_data]))
            }
    
    async def _generate_sales_recommendations(self, products_data: List[Dict], analyses: List[Dict]) -> Dict[str, Any]:
        """Satış önerileri oluştur"""
        try:
            # Analiz sonuçlarından önemli bilgileri çıkar
            total_reviews = sum([len(p.get('reviews', [])) for p in products_data])
            marketplaces = list(set([p.get('domain', 'Bilinmeyen') for p in products_data]))
            
            # Yorum analizlerinden insight'ları topla
            all_pros = []
            all_cons = []
            all_themes = []
            
            for analysis in analyses:
                review_analysis = analysis.get('review_analysis', {})
                all_pros.extend(review_analysis.get('pros', []))
                all_cons.extend(review_analysis.get('cons', []))
                all_themes.extend(review_analysis.get('common_themes', []))
            
            # Detaylı prompt oluştur
            prompt = f"""
            E-ticaret danışmanı olarak, aşağıdaki veriler ışığında bu ürünü satmak isteyen bir satıcı için DETAYLI stratejik öneriler oluştur:

            ÜRÜN ANALİZ VERİLERİ:
            - Analiz edilen ürün sayısı: {len(products_data)}
            - Toplam incelenen yorum: {total_reviews}
            - Pazaryerleri: {', '.join(marketplaces)}
            
            MÜŞTERİ GERİ BİLDİRİMLERİ:
            Artı Yönler: {', '.join(all_pros[:10])}
            Eksi Yönler: {', '.join(all_cons[:10])}
            Ana Temalar: {', '.join(all_themes[:10])}

            Lütfen aşağıdaki başlıklar altında DETAYLI ve UYGULANABILIR öneriler sun:

            ## 1. FİYATLANDIRMA STRATEJİSİ
            - Mevcut fiyat pozisyonlaması analizi
            - Rakiplere karşı fiyat stratejisi
            - Dinamik fiyatlandırma önerileri
            - İndirim ve promosyon stratejileri

            ## 2. ÜRÜN PAZARLAMASİ VE REKLAM
            - Ürünün güçlü yönlerini öne çıkaran pazarlama mesajları
            - Hedef müşteri segmentleri
            - Reklam başlıkları ve açıklamalar
            - Sosyal medya stratejisi

            ## 3. MÜŞTERİ MEMNUNİYETİ İYİLEŞTİRME
            - Müşteri şikayetlerini önleme yöntemleri
            - Müşteri hizmetleri iyileştirmeleri
            - Ürün kalitesi geliştirme önerileri
            - After-sales destek stratejisi

            ## 4. REKABET ANALİZİ VE POZİSYONLAMA
            - Rakip analizi ve fark yaratma yöntemleri
            - Benzersiz satış önerisi (USP) geliştirme
            - Pazar pozisyonlama stratejisi
            - Competitive advantage oluşturma

            ## 5. SATIŞ ARTIRMA TAKTİKLERİ
            - Cross-selling ve up-selling fırsatları
            - Bundle ürün önerileri
            - Sezonsal satış stratejileri
            - Stok yönetimi önerileri

            ## 6. RİSK YÖNETİMİ VE ÖNLEMLER
            - Potansiyel problemler ve çözümler
            - Müşteri memnuniyetsizliği önleme
            - Return/iade politikası önerileri
            - Reputation management

            Her başlık altında en az 3-4 spesifik ve uygulanabilir öneri sun. Önerilerin e-ticaret satıcısının hemen uygulayabileceği türden olmasına dikkat et.
            """
            
            response = await asyncio.to_thread(self.model.generate_content, prompt)
            
            return {
                'recommendations_text': response.text.strip(),
                'generated_at': datetime.now().isoformat(),
                'analysis_quality': 'detailed',
                'data_sources': f"{len(products_data)} ürün, {total_reviews} yorum",
                'marketplaces_analyzed': marketplaces
            }
            
        except Exception as e:
            logger.error(f"Satış önerileri hatası: {e}")
            return {
                'recommendations_text': f"""
                # SATIŞÇI İÇİN ÖNERİLER (Basit Analiz)
                
                **Not:** AI analizi şu anda tam olarak çalışamıyor, basit öneriler sunuluyor.
                
                ## Temel Stratejiler:
                
                ### 1. Fiyatlandırma
                - Rakip fiyatlarını düzenli kontrol edin
                - Müşteri yorumlarında fiyat şikayeti varsa değerlendirin
                - İndirim kampanyaları düzenleyin
                
                ### 2. Müşteri Memnuniyeti
                - Yorumları düzenli takip edin
                - Hızlı müşteri hizmetleri sağlayın
                - Ürün kalitesini sürekli iyileştirin
                
                ### 3. Pazarlama
                - Ürünün güçlü yönlerini vurgulayın
                - Müşteri testimoniallarını kullanın
                - Sosyal medyada aktif olun
                
                ### 4. Risk Yönetimi
                - Stok takibi yapın
                - İade politikanızı netleştirin
                - Müşteri şikayetlerine hızlı yanıt verin
                
                **Detaylı analiz için sistem güncellemesi gerekiyor.**
                """,
                'error': True,
                'generated_at': datetime.now().isoformat()
            }
    
    async def _generate_summary(self, products_data: List[Dict], analyses: List[Dict]) -> Dict[str, Any]:
        """Genel özet oluştur"""
        try:
            total_products = len(products_data)
            total_reviews = sum([len(p.get('reviews', [])) for p in products_data])
            marketplaces = list(set([p.get('domain', 'Bilinmeyen') for p in products_data]))
            
            return {
                'total_products_analyzed': total_products,
                'total_reviews_analyzed': total_reviews,
                'marketplaces_covered': marketplaces,
                'analysis_completed_at': datetime.now().isoformat(),
                'summary_text': f"{total_products} ürün analiz edildi, toplam {total_reviews} yorum incelendi."
            }
            
        except Exception as e:
            logger.error(f"Özet oluşturma hatası: {e}")
            return {
                'summary_text': f'Özet oluşturulamadı: {str(e)}',
                'error': True
            }
