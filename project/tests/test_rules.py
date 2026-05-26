"""Юнит-тесты на rules-слой (regex + нормализация).

Эти тесты не требуют ни Tesseract'а, ни Ollama — проверяют чистые
функции из ``src.rules`` на синтетических входах.
"""

import pytest

from src.rules import (
    normalize_serials,
    extract_serials,
    pick_document_code,
    extract_normative_docs,
    final_cleanup,
)

class TestNormalizeSerials:
    def test_empty_input_returns_empty_list(self):
        assert normalize_serials(None) == []
        assert normalize_serials([]) == []

    def test_dedup_and_uppercase(self):
        result = normalize_serials(["g4m0821", "G4M0821", "g4m0822"])
        assert "G4M0821" in result
        assert "G4M0822" in result
        assert len(result) == 2

    def test_drops_too_short(self):

        result = normalize_serials(["AB", "G4M0821"])
        assert "AB" not in result
        assert "G4M0821" in result

    def test_strips_punctuation_edges(self):
        result = normalize_serials(["G4M0821.", ",G4M0822"])
        assert "G4M0821" in result
        assert "G4M0822" in result

class TestPickDocumentCode:
    def test_extracts_trei_code(self):
        text = "Паспорт TREI.421457.001 ПС\nизделия..."
        code = pick_document_code(text)
        assert "TREI" in code or "421457" in code

    def test_returns_empty_on_no_code(self):
        assert pick_document_code("просто какой-то текст без кодов") == ""

class TestExtractSerials:
    def test_finds_alphanumeric_serial_in_text(self):
        text = "Заводской номер: G4M0821\nДата выпуска: 10.07.2024"
        serials = extract_serials(text)
        assert any("G4M0821" in s for s in serials)

class TestFinalCleanup:
    def test_cleanup_returns_dict_with_quality_score(self):
        data = {"naimenovanie": "  Тестовое  изделие  ", "zavodskie_nomera": ["G4M0821"]}
        result = final_cleanup(data, raw_text="", source_name="test.pdf")
        assert isinstance(result, dict)
        assert "quality_score" in result
        assert isinstance(result["quality_score"], int)

    def test_cleanup_returns_known_schema_keys(self):

        result = final_cleanup({}, raw_text="", source_name="test.pdf")
        for key in ("naimenovanie", "kod_dokumenta", "zavodskie_nomera",
                    "data_vypuska", "proizvoditel", "document_type"):
            assert key in result, f"missing key in cleaned payload: {key}"

class TestNormativeDocs:
    def test_finds_gost_reference(self):
        text = "Соответствует требованиям ГОСТ 12345-99 и ТУ 12.34.567-2020"
        docs = extract_normative_docs(text)
        assert isinstance(docs, list)

        assert len(docs) >= 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
