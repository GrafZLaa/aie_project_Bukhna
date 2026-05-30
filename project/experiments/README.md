# experiments/

Журнал прогонов.

```
experiments/
└── runs/
    ├── exp_001_baseline/        OCR + правила, без LLM
    │   ├── config.yaml
    │   └── metrics.json
    └── exp_002_improved/        то же + опциональный LLM-доскан
        ├── config.yaml
        └── metrics.json
```

Здесь — компактно: что прогонял, с какими параметрами, какие цифры получились. Полные JSON-ответы со всеми samples лежат рядом в `../artifacts/` (`eval_baseline.json`, `eval_improved.json`). Сводный журнал — `../artifacts/experiments_log.json`.

## Если хочется добавить новый запуск

1. Создать папку `runs/exp_NNN_my_change/`.
2. Прогнать `GET /api/evaluate/default?fast=...` или свой сценарий, сохранить полный JSON в `../artifacts/eval_my_change.json`.
3. Заполнить `config.yaml` (что меняли) и `metrics.json` (итоговые цифры).
4. Добавить запись в `../artifacts/experiments_log.json`.
