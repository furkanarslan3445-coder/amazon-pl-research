import json
import signal
import sys
import time
from datetime import date, datetime, timedelta
from config import CONFIG, SEED_KEYWORDS
from category_crawler import crawl_categories
from autocomplete import expand_keywords
from scraper import search_keyword
from analyzer import analyze
from exporter import save_opportunity
from utils import random_delay, logger


def load_json(path: str, default) -> any:
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def save_json(path: str, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def handle_exit(sig, frame):
    logger.info("Durduruluyor... state kaydedildi.")
    sys.exit(0)


def load_done(path: str) -> dict:
    """Done listesini {keyword: tarih_str} formatında yükle.
    Eski format (liste) ise bugünün tarihiyle migrate et."""
    raw = load_json(path, {})
    if isinstance(raw, list):
        today = date.today().isoformat()
        migrated = {kw: today for kw in raw}
        save_json(path, migrated)
        logger.info(f"Done listesi migrate edildi: {len(migrated)} keyword → tarih bazlı format.")
        return migrated
    return raw


def is_due_for_rescan(scan_date_str: str, rescan_days: int) -> bool:
    """Keyword'ün yeniden taranma zamanı geldi mi?"""
    try:
        scanned = datetime.fromisoformat(scan_date_str).date()
        return (date.today() - scanned).days >= rescan_days
    except Exception:
        return True


def build_keyword_pool() -> list[str]:
    """3 katmanlı keyword türetme."""
    logger.info("=== 3 Katmanlı Keyword Türetme Başlıyor ===")

    # Katman 1: kategori ağacı
    seeds = crawl_categories()
    logger.info(f"Katman 1: {len(seeds)} seed")

    # Katman 2: autocomplete
    all_kws = expand_keywords(seeds, depth=2)
    logger.info(f"Katman 2: {len(all_kws)} keyword")

    return list(all_kws)


def main():
    signal.signal(signal.SIGINT, handle_exit)
    signal.signal(signal.SIGTERM, handle_exit)

    logger.info("Amazon PL Niche Bulucu başlatıldı.")

    rescan_days = CONFIG.get("rescan_days", 90)
    pool = load_json(CONFIG["keywords_pool"], [])
    done = load_done(CONFIG["keywords_done"])

    # İlk çalıştırma veya pool boşsa keyword türet
    if not pool:
        pool = build_keyword_pool()
        save_json(CONFIG["keywords_pool"], pool)
        logger.info(f"Toplam keyword havuzu: {len(pool)}")

    total_found = 0
    cycle = 0

    while True:
        cycle += 1

        # Taranmamış VEYA süresi dolmuş keyword'ler
        remaining = [
            kw for kw in pool
            if kw not in done or is_due_for_rescan(done[kw], rescan_days)
        ]
        rescan_count = sum(1 for kw in remaining if kw in done)
        new_count = len(remaining) - rescan_count
        logger.info(
            f"=== Döngü {cycle} | {len(remaining)} keyword kaldı "
            f"({new_count} yeni, {rescan_count} yeniden tarama) ==="
        )

        if not remaining:
            logger.info("Tüm keyword'ler güncel. Yeni keyword türetiliyor...")
            new_pool = build_keyword_pool()
            new_kws = [kw for kw in new_pool if kw not in pool]
            pool.extend(new_kws)
            pool = list(set(pool))
            save_json(CONFIG["keywords_pool"], pool)
            logger.info(f"{len(new_kws)} yeni keyword eklendi.")
            if not new_kws:
                logger.info("Eklenecek yeni keyword yok, bekleniyor (1 saat)...")
                time.sleep(3600)
            continue

        new_related = []

        for keyword in remaining:
            # Ara
            result = search_keyword(keyword)
            done[keyword] = date.today().isoformat()
            save_json(CONFIG["keywords_done"], done)

            # Katman 3: related searches'i havuza ekle
            for rs in result.get("related_searches", []):
                if rs not in done and rs not in pool:
                    new_related.append(rs)

            # Analiz
            analysis = analyze(keyword, result["products"])
            product_count = analysis["product_count"]
            avg_price     = analysis["avg_price"]
            opp_count     = analysis["opportunity_count"]
            opp_ratio     = analysis["opportunity_ratio"]
            is_opp        = analysis["is_opportunity"]

            # Log
            if product_count == 0:
                logger.info(f'Aranan: "{keyword}" | Ürün bulunamadı (CAPTCHA?)')
            elif is_opp:
                total_found += 1
                logger.info(
                    f'Aranan: "{keyword}" | Ürün: {product_count} | '
                    f'Uygun (fiyat>$40 + yorum<100 + bought≥200): {opp_count}/{product_count} (%{opp_ratio}) | ✅ FIRSAT!'
                )
                save_opportunity(analysis)
            else:
                logger.info(
                    f'Aranan: "{keyword}" | Ürün: {product_count} | '
                    f'Uygun: {opp_count}/{product_count} (%{opp_ratio}) | ❌'
                )

            random_delay()

        # Yeni related search'leri havuza ekle
        if new_related:
            pool.extend(new_related)
            pool = list(set(pool))
            save_json(CONFIG["keywords_pool"], pool)
            logger.info(f"Katman 3: {len(new_related)} yeni related search eklendi.")

        logger.info(f"Döngü {cycle} bitti. Toplam fırsat bulundu: {total_found}")


if __name__ == "__main__":
    main()
