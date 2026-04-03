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

    # Kaç gün sonra keyword yeniden taransın
    "rescan_days": 90,

    # Dosya yolları
    "keywords_pool": "keywords_pool.json",
    "keywords_done": "keywords_done.json",
    "error_log":     "error_log.txt",
    "output_dir":    "output",
    "output_file":   f"output/amazon_niche_rapor_{date.today()}.xlsx",

    # Amazon kategori seed URL'leri
    "category_urls": [
        # Kitchen & Dining
        "https://www.amazon.com/s?i=kitchen&rh=n:284507",
        # Sports & Outdoors
        "https://www.amazon.com/s?i=sporting&rh=n:3375251",
        # Tools & Home Improvement
        "https://www.amazon.com/s?i=tools&rh=n:228013",
        # Beauty & Personal Care
        "https://www.amazon.com/s?i=beauty&rh=n:3760911",
        # Garden & Outdoor
        "https://www.amazon.com/s?i=garden&rh=n:2972638011",
        # Pet Supplies
        "https://www.amazon.com/s?i=pet-supplies&rh=n:2619533011",
        # Office Products
        "https://www.amazon.com/s?i=office-products&rh=n:1064954",
        # Baby Products
        "https://www.amazon.com/s?i=baby-products&rh=n:165796011",
        # Automotive
        "https://www.amazon.com/s?i=automotive&rh=n:15684181",
        # Toys & Games
        "https://www.amazon.com/s?i=toys-and-games&rh=n:165793011",
        # Arts, Crafts & Sewing
        "https://www.amazon.com/s?i=arts-crafts&rh=n:2617941011",
        # Health & Household
        "https://www.amazon.com/s?i=hpc&rh=n:3760901",
        # Musical Instruments
        "https://www.amazon.com/s?i=musical-instruments&rh=n:11091801",
        # Camera & Photo
        "https://www.amazon.com/s?i=photo&rh=n:502394",
        # Electronics Accessories
        "https://www.amazon.com/s?i=electronics&rh=n:172282",
        # Clothing accessories
        "https://www.amazon.com/s?i=fashion&rh=n:7141123011",
        # Luggage & Travel
        "https://www.amazon.com/s?i=luggage&rh=n:9479199011",
        # Patio & Lawn
        "https://www.amazon.com/s?i=lawn-garden&rh=n:3238155011",
        # Industrial & Scientific
        "https://www.amazon.com/s?i=industrial&rh=n:16310091",
        # Home & Kitchen storage
        "https://www.amazon.com/s?i=kitchen&rh=n:1063498",
    ],
}

# Katman 1 hardcoded seed'ler
SEED_KEYWORDS = [
    # Kitchen & Cooking
    "kitchen organizer", "cooking utensil", "baking accessory", "food storage container",
    "cutting board", "spice rack", "dish rack", "kitchen gadget", "kitchen tool",
    "pot rack", "pan organizer", "mug rack", "bowl set", "meal prep container",
    "kitchen mat", "strainer", "peeler", "grater", "silicone kitchen", "bamboo kitchen",
    "stainless steel kitchen", "kitchen scale", "kitchen timer", "kitchen towel holder",
    "knife block", "knife sharpener", "cast iron skillet", "wok pan", "baking sheet",
    "mixing bowl", "salad spinner", "mandoline slicer", "garlic press", "can opener",
    "bottle opener", "wine rack", "coffee organizer", "spice organizer", "pantry organizer",
    "refrigerator organizer", "drawer organizer kitchen", "under sink organizer",

    # Sports & Fitness
    "yoga mat", "resistance band", "workout gear", "gym accessory", "exercise equipment",
    "sports bottle", "jump rope", "foam roller", "ab roller", "pull up bar",
    "kettlebell", "dumbbell", "barbell pad", "weight belt", "gym bag",
    "fitness tracker accessory", "workout gloves", "knee sleeve", "ankle support",
    "yoga block", "yoga strap", "pilates ring", "balance board", "agility ladder",
    "speed rope", "battle rope", "pull up assist band", "push up bar",
    "sit up bar", "gym mat", "exercise bike accessory", "treadmill accessory",

    # Outdoor & Camping
    "camping gear", "hiking accessory", "outdoor cooking", "tent accessory",
    "sleeping bag accessory", "backpack accessory", "water filter", "fire starter",
    "camping lantern", "headlamp", "trekking pole", "carabiner", "hammock",
    "camp chair", "cooler accessory", "fishing gear", "fishing tackle",
    "fishing rod holder", "tackle box", "lure set", "hunting accessory",
    "archery accessory", "binoculars strap", "compass", "survival kit",

    # Tools & Home Improvement
    "tool organizer", "storage rack", "wall mount", "garage organizer",
    "pegboard organizer", "drill bit set", "measuring tape", "level tool",
    "stud finder", "tool belt", "tool bag", "workbench organizer",
    "cable management", "wire organizer", "extension cord organizer",
    "ladder accessory", "safety gear", "dust mask", "safety glasses",
    "magnetic tool holder", "screwdriver set", "wrench set", "pliers set",

    # Beauty & Personal Care
    "hair tool", "hair dryer holder", "curling iron holder", "hair accessory",
    "skincare device", "facial roller", "gua sha", "jade roller", "face mask",
    "nail care kit", "nail art tool", "makeup organizer", "cosmetic bag",
    "beauty blender", "makeup brush set", "eyelash curler", "eyebrow kit",
    "shaving kit", "beard trimmer accessory", "beard care", "hair removal",
    "bath accessory", "shower caddy", "soap dispenser", "loofah",
    "toothbrush holder", "razor holder", "cotton swab organizer",

    # Garden & Outdoor
    "garden tool", "planter pot", "raised garden bed", "garden kneeler",
    "garden gloves", "garden hose", "hose nozzle", "sprinkler",
    "plant stand", "flower pot", "seed starter", "garden marker",
    "compost bin", "garden cart", "watering can", "pruning shears",
    "garden apron", "bird feeder", "bird bath", "wind chime",
    "outdoor planter", "hanging basket", "trellis", "garden fence",
    "soil scoop", "transplant tool", "bulb planter", "lawn edger",

    # Pet Supplies
    "dog accessory", "cat toy", "pet feeder", "pet water fountain",
    "pet grooming brush", "dog harness", "cat bed", "dog bed",
    "pet carrier", "dog training clicker", "cat scratcher", "dog leash",
    "pet food container", "dog treat pouch", "pet first aid", "dog poop bag",
    "cat litter mat", "dog crate cover", "pet gate", "dog playpen",
    "cat tunnel", "dog puzzle toy", "interactive pet toy", "fish tank accessory",
    "aquarium decoration", "reptile accessory", "bird cage accessory",

    # Office & Desk
    "desk organizer", "monitor stand", "laptop stand", "keyboard wrist rest",
    "mouse pad", "cable management desk", "desk mat", "monitor arm",
    "ergonomic accessory", "office storage", "filing organizer", "pen holder",
    "sticky note organizer", "whiteboard accessory", "bulletin board",
    "desk lamp", "ring light", "webcam cover", "phone stand", "tablet stand",
    "document holder", "book stand", "magazine holder", "mail organizer",

    # Baby & Kids
    "baby carrier", "baby monitor accessory", "diaper bag", "baby feeding set",
    "baby bath accessory", "stroller accessory", "baby play mat", "baby gym",
    "teething toy", "baby night light", "nursing pillow", "bottle warmer",
    "baby food maker", "baby food storage", "sippy cup", "toddler cutlery",
    "kids water bottle", "kids lunch box", "kids art supply",
    "sensory toy", "montessori toy", "wooden toy", "learning toy",

    # Automotive
    "car organizer", "car seat organizer", "trunk organizer", "car phone mount",
    "car charger", "car air freshener", "steering wheel cover", "car mat",
    "windshield sunshade", "car cleaning kit", "tire inflator", "jump starter",
    "dash cam mount", "car trash can", "backseat organizer", "car cup holder",
    "car key holder", "parking sensor", "car seat gap filler", "car headrest hook",

    # Arts & Crafts
    "art supply organizer", "paintbrush set", "canvas board", "sketching set",
    "watercolor set", "acrylic paint set", "calligraphy set", "lettering kit",
    "scrapbook supply", "washi tape", "craft storage", "sewing kit",
    "embroidery kit", "cross stitch kit", "knitting accessory", "crochet hook set",
    "macrame kit", "resin kit", "diamond painting", "clay sculpting tool",

    # Health & Wellness
    "massage tool", "massage gun accessory", "foam roller", "acupressure mat",
    "posture corrector", "back support", "lumbar pillow", "neck pillow",
    "eye mask", "sleep aid", "essential oil diffuser", "humidifier accessory",
    "first aid kit", "pill organizer", "blood pressure cuff", "thermometer",
    "pulse oximeter", "heating pad", "cold pack", "compression sock",
    "knee brace", "wrist brace", "back brace", "ankle brace",

    # Musical Instruments
    "guitar accessory", "guitar strap", "guitar pick", "guitar stand",
    "ukulele accessory", "piano accessory", "drum accessory", "drum stick",
    "microphone stand", "music stand", "metronome", "tuner",
    "capo", "slide guitar", "violin accessory", "trumpet mute",

    # Photography
    "camera strap", "camera bag", "lens filter", "tripod accessory",
    "camera cleaning kit", "memory card case", "battery grip", "remote shutter",
    "camera mount", "phone camera lens", "lighting accessory", "reflector",
    "backdrop stand", "prop box", "drone accessory",

    # Travel & Luggage
    "packing cube", "travel organizer", "passport holder", "luggage tag",
    "travel pillow", "travel blanket", "travel bottle set", "toiletry bag",
    "cable organizer travel", "travel adapter", "luggage strap", "bag scale",
    "travel wallet", "rfid blocking wallet", "money belt", "travel shoe bag",

    # Home Organization
    "closet organizer", "shoe rack", "handbag organizer", "belt organizer",
    "tie organizer", "jewelry organizer", "makeup storage", "bathroom organizer",
    "medicine cabinet organizer", "laundry organizer", "hamper", "clothespin bag",
    "ironing board cover", "vacuum storage bag", "storage bin", "basket organizer",
    "shelf divider", "drawer insert", "lazy susan", "turntable organizer",

    # Electronics Accessories
    "cable organizer", "charging station", "wireless charger pad", "power bank case",
    "earbud case", "headphone stand", "speaker stand", "tv mount",
    "surge protector", "smart home accessory", "gaming accessory", "controller stand",
    "gaming headset stand", "keyboard cover", "screen protector applicator",

    # Cleaning & Household
    "cleaning brush set", "scrub brush", "mop accessory", "broom holder",
    "cleaning caddy", "spray bottle set", "microfiber cloth set", "squeegee",
    "toilet brush", "bathroom scrubber", "kitchen sponge holder", "soap dispenser set",
    "garbage bag organizer", "recycling bin", "dust pan set",
]
