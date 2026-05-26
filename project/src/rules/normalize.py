"""Нормализация серийных номеров (правила без глобального состояния).

Самодостаточный модуль — зависит только от ``re`` и констант из
``_constants``. Используется и из ``app/app.py``, и из тестов/ноутбуков
напрямую как ``from src.rules.normalize import normalize_serials``.
"""

from __future__ import annotations

import re
from typing import List, Optional

from src.rules._constants import CYR_TO_LAT_LOOKALIKE, SERIAL_CONFUSABLES

def _normalize_serial_token(token: str) -> str:
    """Привести один токен к канонической форме: верхний регистр, без
    пробелов и краевой пунктуации, кириллические двойники → латиница."""
    t = re.sub(r"\s+", "", str(token or "").upper()).strip(" .,;:()[]{}")
    return t.translate(CYR_TO_LAT_LOOKALIKE)

def _is_probable_serial(token: str) -> bool:
    """Эвристический фильтр: похоже ли слово на заводской номер."""
    t = token.strip(" .,;:()[]{}").upper()
    if not t or not re.search(r"\d", t):
        return False
    if re.match(r"^(ТУ|TY|ТY)[A-ZА-Я0-9\-]{4,}$", t):
        return False
    if re.fullmatch(r"[A-ZА-Я]{2,8}\.\d{3,6}\.\d{2,4}(?:-\d{2,3})?[A-ZА-Я]{0,3}", t):
        return False
    if len(t) < 4 or len(t) > 20:
        return False
    if re.fullmatch(r"\d{1,5}", t):
        return False
    if re.fullmatch(r"\d{6,7}", t):
        return False
    if re.fullmatch(r"(19|20)\d{2}", t):
        return False
    if re.fullmatch(r"\d{1,2}\.\d{1,2}\.\d{2,4}", t):
        return False
    if re.fullmatch(r"\d{8,15}", t):
        return True
    if re.fullmatch(r"[A-ZА-Я]{2,4}\d{3,4}", t):
        return False
    if re.search(r"\d+[XХ]\d+[XХ]\d+", t):
        return False
    if not re.fullmatch(r"[A-ZА-Я0-9\-]{5,20}", t):
        return False
    digit_count = len(re.findall(r"\d", t))
    letter_count = len(re.findall(r"[A-ZА-Я]", t))
    if len(t) < 7 or digit_count < 3 or letter_count < 1:
        return False
    return bool(re.search(r"\d{4,}", t))

def _is_table_serial_candidate(token: str) -> bool:
    """Более мягкий фильтр для серийников из табличных колонок."""
    t = _normalize_serial_token(token)
    if not t:
        return False
    if re.fullmatch(r"\d{6,12}", t):
        return True
    if re.fullmatch(r"[A-Z]\d[A-Z]\d{3,8}", t):
        return True
    if not re.fullmatch(r"[A-Z0-9\-]{5,20}", t):
        return False
    digit_count = len(re.findall(r"\d", t))
    letter_count = len(re.findall(r"[A-Z]", t))
    if digit_count < 4:
        return False
    return letter_count <= digit_count

def _serial_plausibility_score(token: str) -> int:
    """Оценка «качества» серийника: используется при выборе лучшего из
    OCR-кандидатов (1/I, 5/S, 8/B и т.п.)."""
    t = _normalize_serial_token(token)
    score = 0
    if re.match(r"^[A-Z][0-9]", t):
        score += 4
    if re.match(r"^[A-Z][0-9][A-Z][0-9]{3,}$", t):
        score += 5
    if re.search(r"\d{4,}", t):
        score += 3
    if re.search(r"[A-Z]", t):
        score += 2
    if t and t[0].isdigit() and re.search(r"[A-Z]", t):
        score -= 3
    if t.count("-") > 1:
        score -= 1
    return score

def _serial_candidates(token: str) -> List[str]:
    """Сгенерировать правдоподобные варианты замены confusables в первых
    4 символах токена (там OCR ошибается чаще всего)."""
    base = _normalize_serial_token(token)
    if not re.search(r"[A-Z]", base):
        return [base]
    candidates = {base}
    for pos, ch in enumerate(base[:4]):
        alt = SERIAL_CONFUSABLES.get(ch)
        if not alt:
            continue
        candidates.add(base[:pos] + alt + base[pos + 1:])
    return [c for c in candidates if c]

def _canonicalize_serial(token: str) -> str:
    """Выбрать из confusable-кандидатов наиболее правдоподобный."""
    candidates = []
    for cand in _serial_candidates(token):
        if _is_probable_serial(cand):
            candidates.append(cand)
    if not candidates:
        return _normalize_serial_token(token)
    return max(candidates, key=_serial_plausibility_score)

def normalize_serials(serials: Optional[List[str]]) -> List[str]:
    """Финальная нормализация списка серийников: дедуп, фильтр коротких,
    канонизация регистра/буквенных двойников."""
    if not serials:
        return []
    seen = set()
    result = []
    for raw in serials:
        s = re.sub(r"\s+", "", str(raw or "").upper())
        s = s.strip(".,;:-")
        if re.fullmatch(r"[A-ZА-Я0-9\-]{3,24}", s):
            s = s.translate(CYR_TO_LAT_LOOKALIKE)
        if len(s) < 3:
            continue
        if s not in seen:
            seen.add(s)
            result.append(s)
    return result

__all__ = [
    "_normalize_serial_token",
    "_is_probable_serial",
    "_is_table_serial_candidate",
    "_serial_plausibility_score",
    "_serial_candidates",
    "_canonicalize_serial",
    "normalize_serials",
]
