"""LLM-слой: опциональная доскан-обработка локальной мультимодальной моделью.

Используется Ollama (``/api/generate``), никаких облачных API. Если
LLM выключена (``ENABLE_LLM=0``), недоступна или вернула таймаут —
пайплайн прозрачно откатывается на чистый OCR + правила.

Этот слой в терминах курса — «улучшенная модель» поверх baseline'а.
"""

from src._core import _core as _c

resolve_llm_backend = _c.resolve_llm_backend
is_ollama_reachable = _c.is_ollama_reachable
choose_active_ollama_model = _c.choose_active_ollama_model
get_available_ollama_models = _c.get_available_ollama_models

run_llm_extraction = _c.run_llm_extraction
run_ollama_extraction = _c.run_ollama_extraction
prepare_llm_images_b64 = _c.prepare_llm_images_b64

clean_json = _c.clean_json

__all__ = [
    "resolve_llm_backend",
    "is_ollama_reachable",
    "choose_active_ollama_model",
    "get_available_ollama_models",
    "run_llm_extraction",
    "run_ollama_extraction",
    "prepare_llm_images_b64",
    "clean_json",
]
