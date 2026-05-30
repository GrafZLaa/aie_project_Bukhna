# data/

Runtime-данные сервиса. В репо здесь только `.gitkeep` и это описание.

## Что появляется при запуске

- `registry_state.json` — реестр обработанных паспортов, создаётся сервисом сам. В `.gitignore`.
- `feedback_log.jsonl` — журнал отзывов через `/api/feedback`. Тоже в `.gitignore`.

## Демо-документы

Демо-PDF лежат рядом в `../приложения/`. Их я использую в ноутбуках `01_eda.ipynb` и `02_baselines.ipynb` и в контрольной выборке `samples/control_samples.json`.

Свои PDF для проверки сюда класть не нужно — подаю через UI на `http://localhost:5000` или POST'ом на `/api/extract` (он же `/predict`). Реестр и логи запишутся сюда же.
