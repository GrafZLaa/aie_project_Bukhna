"""Сравнение predicted vs expected при оценке на контрольной выборке.

Чистые функции — без глобального состояния, без зависимостей от
``app/app.py``. Используются и из ``_extract_document_payload`` (внутри
``_evaluate_samples`` в ``app.py``), и из тестов/ноутбуков.
"""

from __future__ import annotations

import re
from typing import Any

def _as_bool(value: Any, default: bool = False) -> bool:
    """Приведение свободного значения к bool по правилу 1/true/yes/y/on."""
    if isinstance(value, bool):
        return value
    if value is None:
        return default
    s = str(value).strip().lower()
    if s in {"1", "true", "yes", "y", "on"}:
        return True
    if s in {"0", "false", "no", "n", "off"}:
        return False
    return default

def _normalize_eval_scalar(value: Any) -> str:
    """Канонизация скаляра для сравнения: lower, ё→е, схлопывание пробелов."""
    if value is None:
        return ""
    return re.sub(r"\s+", " ", str(value).replace("ё", "е").lower()).strip()

def _compare_eval_value(expected: Any, predicted: Any) -> bool:
    """Сравнение значения поля с эталоном.

    Для списков — поэлементное сравнение нормализованных значений
    (порядок не важен). Для скаляров — равенство нормализованных строк.
    """
    if isinstance(expected, list):
        exp = sorted(_normalize_eval_scalar(x) for x in expected if _normalize_eval_scalar(x))
        pred = sorted(
            _normalize_eval_scalar(x)
            for x in (predicted or [])
            if _normalize_eval_scalar(x)
        )
        return exp == pred
    return _normalize_eval_scalar(expected) == _normalize_eval_scalar(predicted)

__all__ = ["_as_bool", "_normalize_eval_scalar", "_compare_eval_value"]
