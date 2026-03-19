"""Generate README-safe visuals from audited local figures."""

import json
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RESULTS = ROOT / "results_summary.json"
OUTPUT = ROOT / "reports" / "readme_verified_summary.png"


def load_figures() -> dict:
    """Load the figures dict from results_summary.json."""
    data = json.loads(RESULTS.read_text())
    return data["figures"]


def build_chart(figures: dict) -> None:
    """Render a two-panel wage-context chart and save it to reports/."""
    hhsc_wage = figures["hhsc_target_wage"]["value"]
    bls_mean = figures["bls_tx_hha_mean_wage"]["value"]
    cpi_parity = figures["inflation_adjusted_wage"]["value"]
    real_value = figures["real_purchasing_power"]["value"]
    erosion_pct = figures["purchasing_power_lost_pct"]["value"]

    plt.style.use("seaborn-v0_8-whitegrid")
    fig, axes = plt.subplots(1, 2, figsize=(13, 5), gridspec_kw={"width_ratios": [1.45, 1]})

    context_labels = [
        "HHSC published base wage",
        "BLS TX mean wage\nSOC 31-1120 (May 2024)",
        "2025 CPI parity\nfor a $10.60 2015 wage",
    ]
    context_values = [hhsc_wage, bls_mean, cpi_parity]
    context_colors = ["#c0392b", "#2980b9", "#2e8b57"]

    left = axes[0]
    bars = left.barh(context_labels, context_values, color=context_colors, height=0.62)
    left.set_title("Audited Wage Context", fontsize=15, weight="bold")
    left.set_xlabel("Hourly wage ($)")
    left.set_xlim(0, 16)
    left.invert_yaxis()
    left.grid(axis="x", alpha=0.25)
    left.spines["top"].set_visible(False)
    left.spines["right"].set_visible(False)

    for bar, value in zip(bars, context_values):
        left.text(
            value + 0.2,
            bar.get_y() + bar.get_height() / 2,
            f"${value:.2f}",
            va="center",
            fontsize=11,
            weight="bold",
        )

    right = axes[1]
    purchasing_labels = ["Nominal wage", "Real value\n(2015 dollars)"]
    purchasing_values = [hhsc_wage, real_value]
    purchasing_colors = ["#c0392b", "#6c8ebf"]
    bars = right.bar(purchasing_labels, purchasing_values, color=purchasing_colors, width=0.58)
    right.set_title("Purchasing Power in 2025", fontsize=15, weight="bold")
    right.set_ylabel("Hourly wage ($)")
    right.set_ylim(0, 12)
    right.grid(axis="y", alpha=0.25)
    right.spines["top"].set_visible(False)
    right.spines["right"].set_visible(False)

    for bar, value in zip(bars, purchasing_values):
        right.text(
            bar.get_x() + bar.get_width() / 2,
            value + 0.2,
            f"${value:.2f}",
            ha="center",
            fontsize=11,
            weight="bold",
        )

    right.annotate(
        f"{erosion_pct:.1f}% less buying power",
        xy=(1, real_value),
        xytext=(0.9, 10.3),
        textcoords="data",
        arrowprops={"arrowstyle": "->", "color": "#444444", "lw": 1.4},
        ha="center",
        fontsize=11,
    )

    fig.suptitle(
        "Audited Wage Figures\nOnly source-backed or deterministic figures from this repo",
        fontsize=17,
        weight="bold",
        y=1.02,
    )
    fig.text(
        0.5,
        -0.02,
        (
            "HHSC and BLS values come from checked-in source files. "
            "CPI parity and real value are derived from BLS CPI-U South "
            "using documented formulas."
        ),
        ha="center",
        fontsize=10,
        color="#555555",
    )
    fig.tight_layout()
    fig.savefig(OUTPUT, dpi=180, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    """Generate the README verified-summary chart from results_summary.json."""
    figures = load_figures()
    build_chart(figures)
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
