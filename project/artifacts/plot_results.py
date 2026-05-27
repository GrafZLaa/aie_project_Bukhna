"""Строит графики из eval_baseline.json и eval_improved.json.

Запуск:
    cd project
    python artifacts/plot_results.py

Скрипт читает JSON-результаты двух прогонов и сохраняет:
    artifacts/accuracy_per_field.png — точность по полям, baseline vs improved.
    artifacts/runtime_comparison.png — время прогона, baseline vs improved.
"""

from __future__ import annotations

import json
from pathlib import Path

import matplotlib.pyplot as plt

HERE = Path(__file__).resolve().parent
BASELINE = HERE / "eval_baseline.json"
IMPROVED = HERE / "eval_improved.json"


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def plot_accuracy_per_field(baseline: dict, improved: dict, out: Path) -> None:
    fields = sorted(baseline["per_field"].keys())
    b_vals = [baseline["per_field"][f]["accuracy_pct"] for f in fields]
    i_vals = [improved["per_field"][f]["accuracy_pct"] for f in fields]

    x = range(len(fields))
    width = 0.38

    fig, ax = plt.subplots(figsize=(11, 5))
    ax.bar([p - width / 2 for p in x], b_vals, width, label="baseline", color="#3b82f6")
    ax.bar([p + width / 2 for p in x], i_vals, width, label="improved", color="#10b981")

    ax.set_ylabel("Accuracy, %")
    ax.set_ylim(0, 110)
    ax.set_xticks(list(x))
    ax.set_xticklabels(fields, rotation=20, ha="right")
    ax.set_title("Field-level accuracy on control set (6 PDF, 20 checks)")
    ax.legend(loc="lower right")
    ax.grid(axis="y", alpha=0.3)

    for p, v in zip(x, b_vals):
        ax.text(p - width / 2, v + 1.5, f"{v:.0f}%", ha="center", fontsize=8)
    for p, v in zip(x, i_vals):
        ax.text(p + width / 2, v + 1.5, f"{v:.0f}%", ha="center", fontsize=8)

    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"  saved: {out.name}")


def plot_runtime_comparison(baseline: dict, improved: dict, out: Path) -> None:
    labels = ["baseline\n(OCR + rules)", "improved\n(+ LLM available)"]
    times = [baseline["elapsed_sec"], improved["elapsed_sec"]]
    colors = ["#3b82f6", "#10b981"]

    fig, ax = plt.subplots(figsize=(6, 5))
    bars = ax.bar(labels, times, color=colors, width=0.55)

    ax.set_ylabel("Elapsed time, seconds")
    ax.set_title("Control-set evaluation runtime")
    ax.grid(axis="y", alpha=0.3)

    for bar, t in zip(bars, times):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            t + 0.5,
            f"{t:.1f}s",
            ha="center",
            fontsize=10,
            fontweight="bold",
        )

    ax.text(
        0.5, 0.95,
        f"both: 100% accuracy (20/20 checks)",
        transform=ax.transAxes,
        ha="center",
        fontsize=9,
        style="italic",
        color="#555",
    )

    fig.tight_layout()
    fig.savefig(out, dpi=140)
    plt.close(fig)
    print(f"  saved: {out.name}")


def main() -> None:
    baseline = load(BASELINE)
    improved = load(IMPROVED)

    print("Generating plots...")
    plot_accuracy_per_field(baseline, improved, HERE / "accuracy_per_field.png")
    plot_runtime_comparison(baseline, improved, HERE / "runtime_comparison.png")
    print("Done.")


if __name__ == "__main__":
    main()
