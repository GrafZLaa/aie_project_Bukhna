"""Сервисный слой: Flask-приложение и HTTP-эндпойнты.

Реэкспортирует объект ``app`` (Flask) и ключевую функцию
``extract_document_payload`` — точку входа всего пайплайна (data → OCR
→ rules → LLM → post-processing → scoring).
"""

from src._core import _core as _c

app = _c.app
extract_document_payload = _c._extract_document_payload

__all__ = ["app", "extract_document_payload"]
