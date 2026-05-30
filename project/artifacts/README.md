# artifacts/

Результаты прогонов и графики.

| Файл | Что это |
|---|---|
| `experiments_log.json`     | сводный журнал прогонов baseline и improved (accuracy, время, выбор финальной модели) |
| `eval_baseline.json`       | полный JSON-ответ `GET /api/evaluate/default?fast=1` — baseline |
| `eval_improved.json`       | полный JSON-ответ `GET /api/evaluate/default?fast=0` — improved (LLM доступна) |
| `plot_results.py`          | рисует графики из двух JSON выше |
| `accuracy_per_field.png`   | точность по полям, baseline vs improved |
| `runtime_comparison.png`   | время прогона, baseline vs improved |

## Как пересобрать графики

```bash
cd project
python artifacts/plot_results.py
```

## Про модели

Свои веса не учил. Использую готовые: Tesseract (системная зависимость) и Ollama / `llama3.2-vision` (тянется через `ollama pull` в Docker-volume). Поэтому файлов вроде `*.pt` или `*.cbm` здесь нет — это результаты прогонов и выгрузки.

Сюда же можно сохранить Excel-выгрузку (`/api/export/excel`), 1С-JSON (`/api/export/1c_json`) или скриншоты UI после защиты.
