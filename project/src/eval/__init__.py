"""Слой оценки качества на контрольной выборке.

* :mod:`src.eval.compare` — **физически выделенный** модуль с чистыми
  функциями сравнения predicted vs expected.
* Прогон по контролю (``evaluate_samples``, ``predict_for_control_sample``)
  пока живёт в ``app/app.py``, реэкспортируется лениво через
  :mod:`src._core`.
"""

from src.eval.compare import (
    _as_bool,
    _normalize_eval_scalar,
    _compare_eval_value,
)

compare_eval_value = _compare_eval_value
normalize_eval_scalar = _normalize_eval_scalar

def __getattr__(name):
    from src._core import _core
    mapping = {
        "evaluate_samples": "_evaluate_samples",
        "predict_for_control_sample": "_predict_for_control_sample",
    }
    if name in mapping:
        return getattr(_core, mapping[name])
    raise AttributeError(f"module 'src.eval' has no attribute {name!r}")

__all__ = [
    "_as_bool",
    "_normalize_eval_scalar",
    "_compare_eval_value",
    "compare_eval_value",
    "normalize_eval_scalar",
    "evaluate_samples",
    "predict_for_control_sample",
]
