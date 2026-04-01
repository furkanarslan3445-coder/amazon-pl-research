import requests
from utils import get_headers, random_delay, logger

AUTOCOMPLETE_URL = "https://completion.amazon.com/api/2017/suggestions"


def get_suggestions(keyword: str) -> list[str]:
    """Amazon autocomplete'den öneri listesi çek."""
    params = {
        "mid":    "ATVPDKIKX0DER",
        "alias":  "aps",
        "prefix": keyword,
    }
    try:
        r = requests.get(
            AUTOCOMPLETE_URL,
            headers=get_headers(),
            params=params,
            timeout=10,
        )
        r.raise_for_status()
        data = r.json()
        suggestions = [s["value"] for s in data.get("suggestions", [])]
        return suggestions
    except Exception as e:
        logger.error(f"Autocomplete hata [{keyword}]: {e}")
        return []


def expand_keywords(seeds: list[str], depth: int = 2) -> set[str]:
    """
    Seed listesini autocomplete ile genişlet.
    depth=2: her seed → öneri → önerilerin önerileri
    """
    pool = set(seeds)
    current_level = set(seeds)

    for level in range(depth):
        next_level = set()
        logger.info(f"Autocomplete genişletme — seviye {level+1}, {len(current_level)} keyword")
        for kw in current_level:
            suggestions = get_suggestions(kw)
            new = set(suggestions) - pool
            pool.update(new)
            next_level.update(new)
            random_delay()

        current_level = next_level
        if not current_level:
            break

    return pool
