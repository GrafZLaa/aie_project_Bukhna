"""Тесты на структуру контрольного набора и компаратор значений."""

import json
from pathlib import Path

import pytest

from src.eval import compare_eval_value, normalize_eval_scalar

SAMPLES_FILE = Path(__file__).resolve().parents[1] / "samples" / "control_samples.json"

def test_control_samples_file_is_valid_json():
    assert SAMPLES_FILE.exists(), f"missing {SAMPLES_FILE}"
    with SAMPLES_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    assert "samples" in data
    assert isinstance(data["samples"], list)
    assert len(data["samples"]) > 0

def test_each_sample_has_filename_and_expected():
    with SAMPLES_FILE.open("r", encoding="utf-8") as f:
        data = json.load(f)

    for sample in data["samples"]:
        assert "filename" in sample
        assert "expected" in sample
        assert isinstance(sample["expected"], dict)

@pytest.mark.parametrize(
    "expected, predicted, should_match",
    [
        ("TREI.421457.001", "TREI.421457.001", True),
        ("TREI.421457.001", "trei.421457.001", True),
        ("TREI.421457.001", "  TREI.421457.001  ", True),
        ("TREI.421457.001", "ABCD.000000.001", False),
        ("", "", True),
    ],
)
def test_compare_eval_value_scalar(expected, predicted, should_match):
    assert compare_eval_value(expected, predicted) is should_match

def test_compare_eval_value_list_equal():
    assert compare_eval_value(["G4M0821"], ["G4M0821"]) is True
    assert compare_eval_value(["G4M0821"], ["G4M0822"]) is False

def test_normalize_eval_scalar_strips_and_lowercases():
    assert normalize_eval_scalar("  TREI  ") == normalize_eval_scalar("trei")
