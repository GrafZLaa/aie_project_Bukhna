# Самопроверка проекта (self-checklist)

Проект: **ПАСПОРТ.ЦИФ** — извлечение данных из PDF паспортов оборудования.

| #  | Критерий                                                                                | Да/Нет | Где смотреть                                                                                                       |
|----|------------------------------------------------------------------------------------------|--------|---------------------------------------------------------------------------------------------------------------------|
| 1  | Сервис запускается по инструкциям из `README.md` и работает                              | ✅     | [`README.md`](./README.md) §4, [`scripts/start.bat`](./scripts/start.bat), [`scripts/start.sh`](./scripts/start.sh) |
| 2  | Endpoint `/predict` использует **реальную модель**, а не заглушку                        | ✅     | [`app/app.py`](./app/app.py) `predict()` → `extract()` → `_extract_document_payload` (OCR+правила+LLM)             |
| 3  | Есть EDA и хотя бы один эксперимент с метриками                                          | ✅     | [`notebooks/01_eda.ipynb`](./notebooks/01_eda.ipynb), [`notebooks/02_baselines.ipynb`](./notebooks/02_baselines.ipynb), [`report.md`](./report.md) §3, §5 |
| 4  | Есть baseline и улучшенная модель, есть **сравнение по метрикам**                        | ✅     | baseline (OCR+правила) vs improved (+ LLM) в [`notebooks/02_baselines.ipynb`](./notebooks/02_baselines.ipynb) и [`report.md`](./report.md) §5 |
| 5  | Код не свален в один ноутбук: есть внятная структура в `src/`                            | ✅     | Чистые leaf-функции физически вынесены: [`src/rules/normalize.py`](./src/rules/normalize.py), [`src/rules/dates.py`](./src/rules/dates.py), [`src/rules/_constants.py`](./src/rules/_constants.py), [`src/eval/compare.py`](./src/eval/compare.py). Остальные слои ([`src/ocr`](./src/ocr/), [`src/llm`](./src/llm/), [`src/data`](./src/data/), [`src/service`](./src/service/)) реэкспортируют функционал из [`app/app.py`](./app/app.py) — оставшийся монолит коротко описан в [`report.md`](./report.md) §8 |
| 6  | Есть Dockerfile **или** понятный сценарий развёртывания без Docker                       | ✅     | [`infra/Dockerfile`](./infra/Dockerfile), [`infra/docker-compose.yml`](./infra/docker-compose.yml), [`scripts/start.sh`](./scripts/start.sh); локальный вариант — [`README.md`](./README.md) §4.2 |
| 7  | Есть `.env.example` и **нет** в репозитории реальных секретов/паролей                    | ✅     | [`.env.example`](./.env.example), [`.gitignore`](./.gitignore) исключает `.env`. Внешних API-ключей нет — Ollama локальная |
| 8  | Реализованы логи/наблюдаемость (хотя бы консольные логи + `/health`)                     | ✅     | `logging` в [`app/app.py`](./app/app.py), endpoint `GET /health`, `GET /api/meta` с диагностикой OCR/LLM, поле `_meta` в каждом ответе extract |
| 9  | В `report.md` **обоснован выбор финальной модели** по результатам экспериментов          | ✅     | [`report.md`](./report.md) §5 «Выбор финальной модели» — гибрид baseline + LLM-доскан по эвристике                  |
| 10 | `README.md` и `report.md` позволяют понять сценарий демонстрации                         | ✅     | [`README.md`](./README.md) §7, [`report.md`](./report.md) §9                                                       |

**Самооценка: 10/10 ✅.**

## Связь с оценкой (ориентир)

- **5–8 баллов → 4** (хороший, рабочий проект).
- **9–10 баллов → 5** (сильный, хорошо проработанный проект).

Окончательное решение — за преподавателем.

## Дополнительные плюсы проекта (поверх чеклиста)

- Сервис целиком автономный (никаких облачных API), что критично для
  промышленного применения (паспорта могут содержать чувствительные
  внутренние коды).
- В каждом ответе extract есть `_evidence` — мини-«объяснимость»: для
  каждого извлечённого поля видно, на какой странице и в каком фрагменте
  оно найдено.
- Контрольная выборка `samples/control_samples.json` оформлена так, что
  можно расширять её самим (формат документирован в [`README.md`](./README.md)
  и в самом файле через примеры).
- Экспорт ориентирован на два сценария интеграции: Excel (для оператора)
  и `/api/export/1c_json` (для системного коннектора в 1С с валидацией).
