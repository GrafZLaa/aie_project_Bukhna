# project/experiments/

Журнал контрольных прогонов, оформленный по шаблону из `aie-course-meta/engineering-notes/ml-experiment-tracking.md` §2.1.

## Структура

```
experiments/
├── README.md                       — этот файл
└── runs/
    ├── exp_001_baseline/           — OCR + правила, без LLM
    │   ├── config.yaml             — параметры запуска
    │   └── metrics.json            — итоговые метрики
    └── exp_002_improved/           — то же + опциональный LLM-доскан
        ├── config.yaml
        └── metrics.json
```

## Как это согласовано с `artifacts/`

Папки `experiments/runs/exp_NNN_*/` — **компактное представление** конкретного запуска: что именно прогоняли, с какими параметрами, какие цифры получили.

Сырые «толстые» JSON-ответы от `/api/evaluate/default` (со всеми samples, evidence, meta) лежат в [`../artifacts/`](../artifacts/) и в `metrics.json` каждого запуска есть ссылка на соответствующий артефакт.

| Запуск | Что в `experiments/runs/` | Полный JSON в `artifacts/` |
|--------|---------------------------|---------------------------|
| `exp_001_baseline` | `config.yaml` + сводный `metrics.json` | [`../artifacts/eval_baseline.json`](../artifacts/eval_baseline.json) |
| `exp_002_improved` | `config.yaml` + сводный `metrics.json` | [`../artifacts/eval_improved.json`](../artifacts/eval_improved.json) |

Сводный журнал всех прогонов — [`../artifacts/experiments_log.json`](../artifacts/experiments_log.json).

## Как добавить новый запуск

1. Создать папку `experiments/runs/exp_NNN_my_change/` (взять следующий свободный номер).
2. Запустить через `GET /api/evaluate/default?fast=...` или собственный сценарий — сохранить полный JSON в `artifacts/eval_my_change.json`.
3. Заполнить `config.yaml` (что именно меняли) и `metrics.json` (итоговые цифры).
4. Обновить запись в `artifacts/experiments_log.json`.
