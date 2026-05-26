"""Rules-слой: regex/правила извлечения полей и нормализация.

Это «baseline-модель» проекта в терминах курса. По OCR-тексту извлекаются
ключевые поля паспорта (наименование, код документа, серийники, даты,
производитель, гарантия и т.п.) с помощью лейблов и регулярных выражений,
после чего значения нормализуются и санитизируются.

Структура:

* :mod:`src.rules.normalize` и :mod:`src.rules.dates` — **физически
  выделенные** чистые модули, не зависят от ``app/app.py``.
* Остальные функции (``_extract_structured_from_text``, ``final_cleanup``,
  ``parse_cabinet_document``, ...) пока живут в ``app/app.py`` и
  реэкспортируются через :mod:`src._core` (ленивый импорт).
"""

from src.rules.normalize import (
    normalize_serials,
    _normalize_serial_token,
    _is_probable_serial,
    _is_table_serial_candidate,
    _serial_plausibility_score,
    _serial_candidates,
    _canonicalize_serial,
)
from src.rules.dates import (
    _is_date_like,
    _is_duration_like,
    _normalize_numeric_date,
    _try_parse_textual_date,
    _extract_dates_from_chunk,
    _extract_version_dates,
    _find_date_near_label,
)

extract_serials_from_chunk = _extract_dates_from_chunk
extract_dates_from_chunk = _extract_dates_from_chunk
is_date_like = _is_date_like
is_duration_like = _is_duration_like
normalize_serial_token = _normalize_serial_token

def __getattr__(name):
    """Ленивый реэкспорт ещё-не-вынесенных функций из app/app.py."""
    from src._core import _core
    mapping = {
        "extract_structured_from_text": "_extract_structured_from_text",
        "parse_cabinet_document": "parse_cabinet_document",
        "extract_serials": "_extract_serials",
        "extract_labeled_factory_serials": "_extract_labeled_factory_serials",
        "regex_fallbacks": "regex_fallbacks",
        "pick_document_code": "_pick_document_code",
        "extract_normative_docs": "_extract_normative_docs",
        "extract_namenovanie": "_extract_namenovanie",
        "extract_dates": "_extract_dates",
        "extract_release_date_from_pages": "_extract_release_date_from_pages",
        "extract_certificate_value": "_extract_certificate_value",
        "sanitize_extracted_payload": "_sanitize_extracted_payload",
        "quality_assessment": "_quality_assessment",
        "final_cleanup": "final_cleanup",
    }
    if name in mapping:
        return getattr(_core, mapping[name])
    raise AttributeError(f"module 'src.rules' has no attribute {name!r}")

__all__ = [

    "normalize_serials",
    "_normalize_serial_token",
    "_is_probable_serial",
    "_is_table_serial_candidate",
    "_serial_plausibility_score",
    "_serial_candidates",
    "_canonicalize_serial",
    "_is_date_like",
    "_is_duration_like",
    "_normalize_numeric_date",
    "_try_parse_textual_date",
    "_extract_dates_from_chunk",
    "_extract_version_dates",
    "_find_date_near_label",

    "extract_structured_from_text",
    "parse_cabinet_document",
    "extract_serials",
    "extract_labeled_factory_serials",
    "regex_fallbacks",
    "pick_document_code",
    "extract_normative_docs",
    "extract_namenovanie",
    "extract_dates",
    "extract_release_date_from_pages",
    "extract_certificate_value",
    "sanitize_extracted_payload",
    "quality_assessment",
    "final_cleanup",
]
