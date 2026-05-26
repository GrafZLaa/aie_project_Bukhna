"""OCR-слой: Tesseract в multi-pass режиме с предобработкой изображения.

Базовая логика: для каждой страницы пробуем несколько вариантов
предобработки (контраст/бинаризация) и несколько PSM-режимов Tesseract,
выбираем лучший по эвристике качества (``ocr_text_quality``).
"""

from src._core import _core as _c

ocr_page_text = _c.ocr_page_text
collect_ocr_texts = _c.collect_ocr_texts
ocr_text_quality = _c.ocr_text_quality

__all__ = [
    "ocr_page_text",
    "collect_ocr_texts",
    "ocr_text_quality",
]
