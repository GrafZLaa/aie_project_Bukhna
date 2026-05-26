"""Внутренний shim для доступа к ещё не вынесенным функциям из ``app/app.py``.

После того как чистые функции (нормализация серийников, парсинг дат,
сравнение eval-значений) уехали в плоские модули ``src/rules/*`` и
``src/eval/compare``, здесь остаётся точка входа для оставшейся
монолитной части (OCR-обвязка, LLM-этап, Flask-роуты, реестр).

Импорт ``_core`` ленивый — он происходит только при обращении к атрибутам,
чтобы избежать круговых зависимостей с ``src/rules/*`` (которые сам app.py
импортирует).
"""

from __future__ import annotations

import importlib
import os
import sys

def _load_app_module():
    here = os.path.dirname(os.path.abspath(__file__))
    app_dir = os.path.abspath(os.path.join(here, "..", "app"))
    if app_dir not in sys.path:
        sys.path.insert(0, app_dir)
    return importlib.import_module("app")

class _LazyCore:
    """Ленивая прокси: при первом обращении к атрибуту подгружает app/app.py."""

    _module = None

    def _ensure(self):
        if self.__class__._module is None:
            self.__class__._module = _load_app_module()
        return self.__class__._module

    def __getattr__(self, name):
        return getattr(self._ensure(), name)

_core = _LazyCore()

__all__ = ["_core"]
