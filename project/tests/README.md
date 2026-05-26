# project/tests/

`pytest`-тесты. Запуск:

```bash
cd project
pytest tests -v
```

| Файл                                  | Что проверяет                                                                |
|---------------------------------------|-------------------------------------------------------------------------------|
| [`test_rules.py`](./test_rules.py)    | Чистые функции rules-слоя: нормализация серийников, кодов документа, нормативов, итоговая очистка payload. |
| [`test_api.py`](./test_api.py)        | Flask smoke: `/health`, `/api/meta`, `/api/extract` (без файла → 400), `/predict` (алиас), отдача индексной страницы. |
| [`test_eval.py`](./test_eval.py)      | Валидность контрольного набора `samples/control_samples.json` и поведение компаратора `compare_eval_value`. |
| [`conftest.py`](./conftest.py)        | Добавляет корень `project/` в `sys.path`, чтобы `from src import ...` работало без установки пакета. |

> Эти тесты не требуют ни Tesseract'а, ни Ollama — они проверяют только
> синтаксис, импорты и логику чистых функций.
