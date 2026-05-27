# project/artifacts/

Сохранённые артефакты прогонов: метрики, журнал экспериментов, графики, выгрузки.

## Что сейчас в папке

| Файл | Что это |
|------|---------|
| `experiments_log.json`        | Сводный журнал контрольных прогонов: baseline vs improved, accuracy, время, причина выбора финальной модели. |
| `eval_baseline.json`          | Полный JSON-ответ `GET /api/evaluate/default?fast=1` — режим baseline (OCR + правила, без LLM). |
| `eval_improved.json`          | Полный JSON-ответ `GET /api/evaluate/default?fast=0` — режим improved (LLM доступна, full scan). |
| `plot_results.py`             | Скрипт генерации графиков из двух JSON выше. |
| `accuracy_per_field.png`      | Bar-chart точности по полям, baseline vs improved (обе 100 %). |
| `runtime_comparison.png`      | Сравнение времени прогона baseline vs improved (26.0 с vs 32.2 с). |

## Как перегенерировать графики

```bash
cd project
python artifacts/plot_results.py
```

Скрипт прочитает `eval_baseline.json` и `eval_improved.json` и пересоздаст обе PNG.

## Замечание о моделях

В этом проекте **не обучаются собственные веса** — используются готовые компоненты:

- **Tesseract** — pretrained OCR (системная зависимость в Docker-образе);
- **Ollama / `llama3.2-vision`** — pretrained мультимодальная LLM, скачивается через `ollama pull` в Docker-volume `ollama_data`.

Поэтому файлов вида `*.cbm`/`*.pt`/`*.onnx` тут нет. Артефакты — это **результаты прогонов** и **выгрузки**.

## Куда ещё имеет смысл сохранять артефакты

- Excel-выгрузка реестра через `POST /api/export/excel` → можно положить как `registry_export.xlsx` после защиты.
- JSON-выгрузка для 1С через `POST /api/export/1c_json` → как `registry_1c.json`.
- Скриншот UI после успешной обработки PDF → как `ui_screenshot.png`.
- Графики `accuracy_per_field.png` и `runtime_comparison.png` — генерируются скриптом (см. следующие коммиты).

Содержимое папки не критично для запуска сервиса; это материалы для отчёта и защиты.
