# project/artifacts/

Папка для сохранённых артефактов: моделей, отчётов прогонов, экспортов.

## Что сюда складывается

В этом проекте **не обучаются собственные веса** — используются готовые
компоненты:

- **Tesseract** — pretrained OCR-движок (системная зависимость);
- **Ollama / `llama3.2-vision`** — pretrained мультимодальная LLM, скачивается
  через `ollama pull` в Docker-volume `ollama_data` (см. `infra/docker-compose.yml`).

Поэтому «весов модели» в классическом смысле для коммита нет. Сюда можно
складывать:

- Excel-отчёты, выгруженные через `/api/export/excel` (`Registry.xlsx`).
- JSON-выгрузки 1С через `/api/export/1c_json`.
- Дампы метрик из `/api/evaluate/default` и из `notebooks/02_baselines.ipynb`.
- Скриншоты UI и логи прогонов для приложений к отчёту.

Содержимое не коммитим (см. `.gitignore`), кроме этого README и `.gitkeep`.
