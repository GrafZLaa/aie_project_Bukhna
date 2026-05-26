"""Слой работы с данными: рендер PDF в изображения и снятие embedded-текста.

Никакой инференс или OCR здесь не выполняется — это «препроцессинг»,
который превращает входной файл (PDF/изображение) в нормализованное
представление для последующих слоёв.
"""

from src._core import _core as _c

pdf_to_images_and_text = _c.pdf_to_images_and_text
improve_image_variants = _c.improve_image_variants

__all__ = [
    "pdf_to_images_and_text",
    "improve_image_variants",
]
