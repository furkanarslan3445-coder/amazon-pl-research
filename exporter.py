import os
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from config import CONFIG


HEADERS = [
    "Anahtar Kelime", "Ürün Sayısı", "Ort. Fiyat ($)",
    "Uygun Ürün Sayısı", "Oran (%)", "Durum"
]

GREEN  = "FF00AA44"
RED    = "FFCC0000"
YELLOW = "FFFFD700"
GRAY   = "FF2D2D2D"


def _get_or_create_wb() -> tuple:
    path = CONFIG["output_file"]
    os.makedirs(CONFIG["output_dir"], exist_ok=True)

    if os.path.exists(path):
        wb = load_workbook(path)
        ws = wb.active
    else:
        wb = Workbook()
        ws = wb.active
        ws.title = "Niche Firsatlari"
        _write_header(ws)

    return wb, ws, path


def _write_header(ws):
    ws.append(HEADERS)
    for cell in ws[1]:
        cell.font      = Font(bold=True, color="FFFFFFFF")
        cell.fill      = PatternFill("solid", fgColor=GRAY)
        cell.alignment = Alignment(horizontal="center")
    ws.column_dimensions["A"].width = 35
    for col in ["B", "C", "D", "E", "F"]:
        ws.column_dimensions[col].width = 18


def save_opportunity(result: dict):
    """Fırsat bulunan keyword'ü Excel'e ekle."""
    wb, ws, path = _get_or_create_wb()

    status = "✅ GİRİLEBİLİR" if result["is_opportunity"] else "❌"
    row = [
        result["keyword"],
        result["product_count"],
        f"${result['avg_price']:.2f}",
        result["opportunity_count"],
        f"{result['opportunity_ratio']}%",
        status,
    ]
    ws.append(row)

    # Son satırı renklendir
    last_row = ws.max_row
    color = GREEN if result["is_opportunity"] else RED
    for cell in ws[last_row]:
        cell.fill = PatternFill("solid", fgColor=color)
        cell.font = Font(color="FFFFFFFF")

    wb.save(path)
