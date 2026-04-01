from config import CONFIG


def analyze(keyword: str, products: list[dict]) -> dict:
    """
    Yeni kriter: sayfadaki ürünlerin %40'ı aynı anda şunları sağlamalı:
      - Fiyat > $40
      - Yorum < 100
      - Bought >= 200/ay
    """
    if not products:
        return {
            "keyword":           keyword,
            "product_count":     0,
            "avg_price":         0,
            "opportunity_count": 0,
            "opportunity_ratio": 0,
            "is_opportunity":    False,
        }

    prices = [p["price"] for p in products if p["price"]]
    avg_price = sum(prices) / len(prices) if prices else 0

    # 3 kriterden en az 2'sini sağlayan ürünler
    def passes(p):
        if not p["bought"]:
            return False
        price_ok  = bool(p["price"]) and p["price"] >= CONFIG["min_avg_price"]
        review_ok = p["reviews"] < CONFIG["max_reviews"]
        bought_ok = p["bought"] >= CONFIG["min_bought"]
        return sum([price_ok, review_ok, bought_ok]) >= 2

    opportunity_products = [p for p in products if passes(p)]

    total = len(products)
    opp_count = len(opportunity_products)
    opp_ratio = opp_count / total if total > 0 else 0

    # Dominant oyuncu kontrolü
    dominant_count = sum(
        1 for p in products if p["reviews"] >= CONFIG["dominant_reviews_threshold"]
    )
    has_dominant = dominant_count >= CONFIG["dominant_max_count"]

    is_opportunity = opp_ratio >= CONFIG["opportunity_ratio"] and not has_dominant

    return {
        "keyword":           keyword,
        "product_count":     total,
        "avg_price":         round(avg_price, 2),
        "opportunity_count": opp_count,
        "opportunity_ratio": round(opp_ratio * 100, 1),
        "is_opportunity":    is_opportunity,
    }
