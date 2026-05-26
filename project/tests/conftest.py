"""Общая настройка тестов: добавляем корень project/ в sys.path,
чтобы импорты ``from src import ...`` работали без установки пакета."""

import os
import sys

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
