"""Парсинг дат из текста паспорта (правила без глобального состояния)."""

from __future__ import annotations

import re
from typing import List

from src.rules._constants import RU_MONTHS

def _is_date_like(value: str) -> bool:
    if not value:
        return False
    if re.search(r"\b[0-3]?\d[./][01]?\d[./](?:19|20)\d{2}\b", value):
        return True
    if re.search(r"\b[0-3]?\d[./][01]?\d[./]\d{2}\b", value):
        return True
    if re.search(r"\b[0-3]?\d\s+[А-Яа-я]{3,}\s+(?:19|20)\d{2}\b", value, flags=re.IGNORECASE):
        return True
    return False

def _is_duration_like(value: str) -> bool:
    if not value:
        return False
    s = re.sub(r"\s+", " ", str(value).lower().replace("ё", "е")).strip(" .,:;")
    if len(s) < 2 or len(s) > 60:
        return False
    if _is_date_like(s):
        return True
    units = r"(год(?:а|ов)?|лет|месяц(?:а|ев)?|сут(?:ки|ок)?|дн(?:ей|я)?|день|недел(?:я|и|ь)|час(?:ов|а)?)"
    num_words = (
        r"(один|одна|два|две|три|четыре|пять|шесть|семь|восемь|девять|"
        r"десять|двенадцать|пятнадцать|двадцать|тридцать|сорок|пятьдесят)"
    )
    has_amount = bool(re.search(r"\d", s) or re.search(num_words, s))
    return bool(has_amount and re.search(units, s))

def _normalize_numeric_date(day: str, month: str, year: str) -> str:
    d = max(1, min(31, int(day)))
    m = max(1, min(12, int(month)))
    y = int(year)
    if y < 100:
        y = 2000 + y if y <= 39 else 1900 + y
    return f"{d:02d}.{m:02d}.{y:04d}"

def _try_parse_textual_date(value: str) -> str:
    """Распарсить «10 ИЮЛ 2024» / «10-июл-24» и т.п. в DD.MM.YYYY."""
    s = (value or "").upper().replace("Ё", "Е")

    s = s.translate({
        ord("A"): "А",
        ord("B"): "В",
        ord("C"): "С",
        ord("E"): "Е",
        ord("H"): "Н",
        ord("K"): "К",
        ord("M"): "М",
        ord("O"): "О",
        ord("P"): "Р",
        ord("T"): "Т",
        ord("X"): "Х",
        ord("Y"): "У",
    })
    m = re.search(r"\b([0-3]?\d)\s*[-./ ]?\s*([А-Я]{3,8})\.?\s*((?:19|20)?\d{2,4})\b", s)
    if not m:
        return ""
    day, month_word, year = m.group(1), m.group(2), m.group(3)
    month_key = next((k for k in RU_MONTHS if month_word.startswith(k)), "")
    if not month_key:
        return ""
    if len(year) == 4 and not year.startswith(("19", "20")):
        return ""
    if len(year) not in (2, 4):
        return ""
    return _normalize_numeric_date(day, RU_MONTHS[month_key], year)

def _extract_dates_from_chunk(chunk: str) -> List[str]:
    found = []
    for m in re.finditer(r"\b([0-3]?\d)[./]([01]?\d)[./]((?:19|20)?\d{2,4})\b", chunk):
        day, month, year = m.group(1), m.group(2), m.group(3)
        if len(year) == 4 and not year.startswith(("19", "20")):
            continue
        if len(year) not in (2, 4):
            continue
        try:
            found.append(_normalize_numeric_date(day, month, year))
        except Exception:
            continue

    textual = _try_parse_textual_date(chunk)
    if textual:
        found.append(textual)
    return list(dict.fromkeys(found))

def _extract_version_dates(text: str) -> set:
    """Даты, рядом с которыми написано «версия» (это не дата выпуска)."""
    result = set()
    for m in re.finditer(r"версия[^\n]{0,50}", text, flags=re.IGNORECASE):
        for d in _extract_dates_from_chunk(m.group(0)):
            result.add(d)
    return result

def _find_date_near_label(lines: List[str], label_patterns: List[str], window: int = 6) -> str:
    for idx, line in enumerate(lines):
        if not any(re.search(pat, line, flags=re.IGNORECASE) for pat in label_patterns):
            continue
        start = max(0, idx - 1)
        end = min(len(lines), idx + 1 + window)
        chunk = " ".join(lines[start:end])
        dates = _extract_dates_from_chunk(chunk)
        if dates:
            return dates[0]
    return ""

__all__ = [
    "_is_date_like",
    "_is_duration_like",
    "_normalize_numeric_date",
    "_try_parse_textual_date",
    "_extract_dates_from_chunk",
    "_extract_version_dates",
    "_find_date_near_label",
]
