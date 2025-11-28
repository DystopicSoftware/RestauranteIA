import re
from typing import Tuple, Dict
from utils.matching import _normalize, _best_match_by_tokens

_NUM_ANY = re.compile(r"(?:\bx\s*(\d+)\b)|(?:\b(\d+)\s*x?\b)", re.IGNORECASE)

def extract_qty(text: str) -> Tuple[int, str]:
    m = _NUM_ANY.search(text)
    if not m:
        return 1, text
    val = m.group(1) or m.group(2)
    try:
        q = int(val)
        start, end = m.span()
        cleaned = (text[:start] + text[end:]).strip()
        return max(q, 1), cleaned
    except:
        return 1, text

def parsear_pedido_libre(entrada: str) -> Dict[str, int]:
    txt = _normalize(entrada)
    partes = [p.strip() for p in re.split(r"[,\;\+]| y | e ", txt) if p.strip()]
    items: Dict[str, int] = {}

    for p in partes:
        qty, sin_qty = extract_qty(p)
        prod, score = _best_match_by_tokens(sin_qty)
        if not prod:
            prod, score = _best_match_by_tokens(p)
        if prod:
            items[prod] = items.get(prod, 0) + qty
    return items

def parse_receta_items(txt: str) -> Dict[str, int]:
    if not txt.strip():
        return {}
    partes = [p.strip() for p in txt.split(",") if p.strip()]
    receta = {}
    for p in partes:
        if ":" not in p:
            continue 
        ing, q = p.split(":", 1)
        ing = ing.strip()
        q = re.sub(r"[^\d]", "", q)
        if q:
            receta[ing] = int(q)
    return receta