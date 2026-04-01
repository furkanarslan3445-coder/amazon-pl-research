import re
import requests
from bs4 import BeautifulSoup
from utils import get_headers, random_delay, logger
from config import CONFIG


def _make_session() -> requests.Session:
    s = requests.Session()
    if CONFIG["proxy"]:
        s.proxies = {"http": CONFIG["proxy"], "https": CONFIG["proxy"]}
    return s


_session = _make_session()
_request_count = 0


def _get(url: str):
    global _session, _request_count

    # Session rotation
    if _request_count > 0 and _request_count % CONFIG["session_rotate_every"] == 0:
        _session = _make_session()
        logger.info("Session yenilendi.")

    try:
        r = _session.get(url, headers=get_headers(), timeout=15)
        _request_count += 1

        # CAPTCHA veya ban tespiti
        if r.status_code in (503, 429) or "captcha" in r.text.lower():
            wait = __import__("random").randint(
                CONFIG["captcha_wait_min"], CONFIG["captcha_wait_max"]
            )
            logger.warning(f"CAPTCHA/ban tespit edildi. {wait}s bekleniyor...")
            __import__("time").sleep(wait)
            return None

        if r.status_code != 200:
            logger.error(f"HTTP {r.status_code}: {url}")
            return None

        return BeautifulSoup(r.text, "lxml")

    except Exception as e:
        logger.error(f"İstek hatası [{url}]: {e}")
        return None


def _parse_price(text: str):
    """'$42.99' → 42.99, EUR fiyatları None döndür"""
    if not text:
        return None
    if "$" not in text:
        return None  # EUR veya başka para birimi, atla
    text = text.replace(",", "").strip()
    m = re.search(r"\$([\d]+\.[\d]{1,2})", text)
    return float(m.group(1)) if m else None


def _parse_bought(text: str) -> int:
    """'1K+ bought in past month' → 1000, '300+ bought...' → 300"""
    if not text:
        return 0
    text = text.lower()
    m = re.search(r"([\d.]+)k\+", text)
    if m:
        return int(float(m.group(1)) * 1000)
    m = re.search(r"([\d,]+)\+", text)
    if m:
        return int(m.group(1).replace(",", ""))
    return 0


def search_keyword(keyword: str) -> dict:
    """
    Amazon'da keyword ara, ilk sayfadaki ürün verilerini çek.
    Döndürür: {"keyword", "products": [...], "related_searches": [...]}
    """
    url = f"https://www.amazon.com/s?k={keyword.replace(' ', '+')}&i=kitchen"
    soup = _get(url)

    if soup is None:
        return {"keyword": keyword, "products": [], "related_searches": []}

    products = []
    related_searches = []

    # Ürün kartları
    cards = soup.select("div[data-component-type='s-search-result']")
    for card in cards:
        # Sponsored ürünleri atla
        sponsored_el = card.select_one("span.s-label-popover-default")
        if sponsored_el and "sponsored" in sponsored_el.get_text(strip=True).lower():
            continue
        # Fiyat
        price_el = card.select_one("span.a-price span.a-offscreen")
        price = _parse_price(price_el.get_text() if price_el else "")

        # Yorum sayısı — "(3.6K)" veya "(1,234)" formatı
        reviews = 0
        review_el = card.select_one("span.s-underline-text")
        if review_el:
            rt = review_el.get_text(strip=True).replace("(", "").replace(")", "").replace(",", "")
            try:
                if "k" in rt.lower():
                    reviews = int(float(rt.lower().replace("k", "")) * 1000)
                else:
                    reviews = int(rt)
            except Exception:
                reviews = 0

        # Bought in past month
        bought_el = card.select_one("span.a-size-base.a-color-secondary")
        bought_text = ""
        if bought_el and "bought" in bought_el.get_text().lower():
            bought_text = bought_el.get_text(strip=True)
        bought = _parse_bought(bought_text)

        if price is not None:
            products.append({
                "price":   price,
                "reviews": reviews,
                "bought":  bought,
            })

    # Related searches (sayfa altı)
    related_els = soup.select("div.s-related-search-carousel-item span, span.a-size-base.s-link-style")
    for el in related_els:
        text = el.get_text(strip=True)
        if text and len(text) > 3:
            related_searches.append(text.lower())

    # Alternatif related searches selector
    if not related_searches:
        for el in soup.select("a[href*='field-keywords']"):
            text = el.get_text(strip=True)
            if text and len(text) > 3 and keyword.lower() not in text.lower():
                related_searches.append(text.lower())

    related_searches = list(set(related_searches))[:20]

    return {
        "keyword":         keyword,
        "products":        products,
        "related_searches": related_searches,
    }
