# tests/

Запуск:

```bash
cd project
pytest tests -v
```

| Файл | Что проверяет |
|---|---|
| `test_rules.py` | чистые функции из rules — нормализация серийников, коды документов, нормативы, очистка payload |
| `test_api.py`   | smoke Flask: `/health`, `/api/meta`, `/api/extract` без файла → 400, `/predict` (alias), отдача индексной страницы |
| `test_eval.py`  | валидность `samples/control_samples.json` и поведение `compare_eval_value` |
| `conftest.py`   | добавляет корень `project/` в `sys.path`, чтобы `from src import ...` работало |

Тесты не требуют ни Tesseract'а, ни Ollama — гоняются через Flask test-client и чистые функции.
