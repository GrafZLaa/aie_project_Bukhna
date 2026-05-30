# src/

Код по слоям.

| Папка | Что внутри |
|---|---|
| `data/`    | рендер PDF в картинки, снятие embedded-текста (PyMuPDF) |
| `ocr/`     | Tesseract multi-pass + предобработка изображения |
| `rules/`   | baseline — regex и лейбловые экстракторы, нормализация |
| `llm/`     | improved — опциональный доскан через Ollama |
| `service/` | Flask `app` и точка входа `extract_document_payload` |
| `eval/`    | прогон контрольной выборки и компаратор значений |

Чистые функции — нормализация серийников, парсинг дат, eval-компаратор, константы — вынес физически в `rules/normalize.py`, `rules/dates.py`, `rules/_constants.py` и `eval/compare.py`. `app/app.py` их импортирует.

Остальные слои реэкспортируют функционал из `app/app.py` через `src/_core.py` (ленивая загрузка).
