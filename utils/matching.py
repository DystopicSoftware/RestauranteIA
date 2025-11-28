import re
import difflib
from typing import Dict, List, Tuple
from data.productos import recetas

# Variables internas
_STOP = {"de","del","la","el","los","las","y","con","a","al","para","un","una","unos","unas"}
_PRODUCT_INDEX = {}

def _normalize(s: str) -> str:
    s = s.lower().strip()
    trans = str.maketrans("áéíóúüñ", "aeiouun")
    s = s.translate(trans)
    s = re.sub(r"\s+", " ", s)
    return s

def _tokens(name: str) -> List[str]:
    n = _normalize(name)
    toks = re.findall(r"[a-z0-9]+", n)
    toks = [t for t in toks if t not in _STOP and len(t) >= 2]
    return toks

def _singularize_simple(tok: str) -> str:
    if tok.endswith("es") and len(tok) > 3:
        return tok[:-2]
    if tok.endswith("s") and len(tok) > 3:
        return tok[:-1]
    return tok

def _build_product_index() -> Dict[str, Dict]:
    idx = {}
    for name in recetas.keys():
        name_norm = _normalize(name)
        toks = _tokens(name_norm)
        core = sorted({_singularize_simple(t) for t in toks})
        idx[name] = {"name": name, "name_norm": name_norm, "tokens": core}
    return idx

def _refresh_index_if_needed():
    global _PRODUCT_INDEX
    if set(_PRODUCT_INDEX.keys()) != set(recetas.keys()):
        _PRODUCT_INDEX = _build_product_index()

def _best_match_by_tokens(fragment: str) -> Tuple[str, float]:
    _refresh_index_if_needed()
    frag_norm = _normalize(fragment)
    frag_toks = {_singularize_simple(t) for t in _tokens(frag_norm)}

    best = (None, 0.0)
    for name, meta in _PRODUCT_INDEX.items():
        core = set(meta["tokens"])
        inter = core.intersection(frag_toks)
        if inter:
            score = len(inter) / max(1, len(core))
            if score > best[1]:
                best = (name, score)

    if best[1] < 0.34:
        candidates = [meta["name_norm"] for meta in _PRODUCT_INDEX.values()]
        close = difflib.get_close_matches(frag_norm, candidates, n=1, cutoff=0.72)
        if close:
            for name, meta in _PRODUCT_INDEX.items():
                if meta["name_norm"] == close[0]:
                    best = (name, 0.72)
    return best

def match_producto(nombre_input: str) -> str | None:
    prod, score = _best_match_by_tokens(nombre_input)
    return prod