from datetime import date

CONFIG = {
    # Fiyat eşiği
    "min_avg_price": 40.0,

    # Düşük rekabet eşiği (yorum sayısı)
    "max_reviews": 100,

    # Yüksek satış eşiği (bought in past month)
    "min_bought": 200,

    # Fırsat oranı (sayfanın en az %40'ı uygun ürün olmalı)
    "opportunity_ratio": 0.40,

    # Dominant oyuncu tespiti: bu eşiğin üzerinde yorumu olan N+ ürün varsa pazar dolu sayılır
    "dominant_reviews_threshold": 1000,
    "dominant_max_count": 4,

    # İstek gecikmesi (saniye)
    "delay_min": 3,
    "delay_max": 8,

    # Kaç aramada bir session yenile
    "session_rotate_every": 25,

    # Saatlik max istek
    "max_requests_per_hour": 110,

    # CAPTCHA sonrası bekleme (saniye)
    "captcha_wait_min": 60,
    "captcha_wait_max": 120,

    # Proxy (opsiyonel, boş bırakınca kullanılmaz)
    "proxy": None,
    # "proxy": "http://user:pass@host:port",

    # Dosya yolları
    "keywords_pool": "keywords_pool.json",
    "keywords_done": "keywords_done.json",
    "error_log":     "error_log.txt",
    "output_dir":    "output",
    "output_file":   f"output/amazon_niche_rapor_{date.today()}.xlsx",

    # Amazon kategori seed URL'leri (birden fazla kategori)
    "category_urls": [
        "https://www.amazon.com/s?i=kitchen&rh=n:284507",
        "https://www.amazon.com/s?i=sporting&rh=n:3375251",
        "https://www.amazon.com/s?i=tools&rh=n:228013",
        "https://www.amazon.com/s?i=beauty&rh=n:3760911",
        "https://www.amazon.com/s?i=garden&rh=n:2972638011",
        "https://www.amazon.com/s?i=pet-supplies&rh=n:2619533011",
        "https://www.amazon.com/s?i=office-products&rh=n:1064954",
        "https://www.amazon.com/s?i=baby-products&rh=n:165796011",
    ],
}

# Katman 1 hardcoded seed'ler
SEED_KEYWORDS = [
    # Kitchen
    "kitchen", "cooking", "baking", "food storage", "kitchen organizer",
    "cutting board", "spice rack", "dish rack", "kitchen gadget", "kitchen tool",
    "pot", "pan", "mug", "bowl", "container", "jar", "tray", "rack", "holder",
    "kitchen mat", "strainer", "peeler", "grater", "mixer", "blender", "bottle",
    "cup", "plate", "utensil", "knife", "chopping", "silicone kitchen",
    "stainless steel kitchen", "bamboo kitchen",
    # Sports & Fitness
    "fitness equipment", "yoga mat", "resistance bands", "workout gear",
    "gym accessories", "exercise equipment", "sports bottle", "jump rope",
    "foam roller", "ab roller", "pull up bar", "kettlebell", "dumbbell",
    # Tools & Home Improvement
    "tool organizer", "storage rack", "wall mount", "garage organizer",
    "workbench", "drill accessories", "measuring tools", "level tool",
    # Beauty & Personal Care
    "hair tools", "skincare device", "nail care", "facial roller",
    "makeup organizer", "beauty accessories", "massage tool",
    # Garden & Outdoor
    "garden tools", "planter pot", "garden organizer", "outdoor furniture",
    "bird feeder", "garden hose", "plant stand", "garden gloves",
    # Pet Supplies
    "dog accessories", "cat toy", "pet feeder", "pet grooming",
    "dog harness", "cat bed", "pet carrier", "dog training",
    # Office
    "desk organizer", "monitor stand", "cable management", "desk accessories",
    "ergonomic accessories", "office storage", "whiteboard",
    # Baby
    "baby carrier", "baby monitor", "diaper bag", "baby feeding",
    "baby bath", "stroller accessories", "baby play mat",
]
