import json
from scraper import search_keyword
from analyzer import analyze
from utils import random_delay, logger

with open("output/opportunities.json") as f:
    rows = json.load(f)

logger.info(f"Toplam {len(rows)} fırsat doğrulanacak...")
valid = []

for i, row in enumerate(rows):
    kw = row["keyword"]
    logger.info(f"[{i+1}/{len(rows)}] Test: {kw}")
    try:
        result = search_keyword(kw)
        analysis = analyze(kw, result["products"])
        if analysis["is_opportunity"]:
            valid.append(row)
            logger.info(f"  ✅ Geçti")
        else:
            logger.info(f"  ❌ Elendi")
        random_delay()
    except Exception as e:
        logger.error(f"  Hata: {e}")
        valid.append(row)  # hata alınca silme

logger.info(f"Sonuç: {len(valid)}/{len(rows)} geçti")
with open("output/opportunities.json", "w") as f:
    json.dump(valid, f, ensure_ascii=False, indent=2)
