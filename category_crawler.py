import requests
from bs4 import BeautifulSoup
from utils import get_headers, random_delay, logger
from config import CONFIG, SEED_KEYWORDS


def crawl_categories(max_depth: int = 2) -> list[str]:
    """
    Amazon Kitchen & Dining alt kategorilerini çek.
    Sol menüdeki kategori isimlerini seed keyword olarak döndür.
    """
    seeds = list(SEED_KEYWORDS)
    visited = set()

    def crawl(url: str, depth: int):
        if depth > max_depth or url in visited:
            return
        visited.add(url)

        try:
            r = requests.get(url, headers=get_headers(), timeout=15)
            if r.status_code != 200:
                return
            soup = BeautifulSoup(r.text, "lxml")

            # Sol menüdeki kategori linkleri
            sidebar = soup.select("div#leftNav, div.a-section.a-spacing-small")
            for section in sidebar:
                links = section.select("a.a-link-normal")
                for link in links:
                    text = link.get_text(strip=True)
                    href = link.get("href", "")
                    if text and len(text) > 2 and text not in seeds:
                        seeds.append(text.lower())
                    # Bir seviye daha derine in
                    if depth < max_depth and href and "/s?" in href:
                        full_url = f"https://www.amazon.com{href}" if href.startswith("/") else href
                        random_delay()
                        crawl(full_url, depth + 1)

        except Exception as e:
            logger.error(f"Kategori crawl hata [{url}]: {e}")

    logger.info("Katman 1: Kategori ağacı crawl ediliyor...")
    for url in CONFIG["category_urls"]:
        crawl(url, depth=1)
    logger.info(f"Katman 1 tamamlandı: {len(seeds)} seed keyword")
    return list(set(seeds))
