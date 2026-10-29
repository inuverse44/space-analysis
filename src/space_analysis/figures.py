"""成果物の図（docs/analysis-plan.md §5：O-01〜O-03）。配色と描き方は cpi-analysis と同じ決まりに従う。"""

from dataclasses import dataclass

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

from .measures import planets_within, reach_ly, stars_within  # noqa: E402
from .sources import ATTRIBUTION_PLANETS, ATTRIBUTION_STARS, EVENTS, FIGURES_DIR, PC_TO_LY, REFERENCE_DATE  # noqa: E402

FONT_CANDIDATES = ["Hiragino Sans", "Noto Sans CJK JP", "BIZ UDGothic", "YuGothic"]

# 近い星の日本語名（HYG の proper / gl から）
STAR_NAMES_JA = {
    "Proxima Centauri": "プロキシマ・ケンタウリ",
    "Rigil Kentaurus": "ケンタウルス座α星A",
    "Toliman": "ケンタウルス座α星B",
    "Barnard's Star": "バーナード星",
    "Wolf 359": "ウォルフ359",
    "Lalande 21185": "ラランド21185",
    "Gl 65A": "ライテン726-8A",
    "Gl 65B": "ライテン726-8B",
    "Sirius": "シリウスA",
    "Gl 244B": "シリウスB",
    "Ross 154": "ロス154",
    "Ross 248": "ロス248",
    "Ran": "エリダヌス座ε星",
    "Lacaille 9352": "ラカイユ9352",
}
ALPHA_CEN = {"Proxima Centauri", "Rigil Kentaurus", "Toliman"}


@dataclass(frozen=True)
class Theme:
    name: str
    surface: str
    ink: str
    ink_secondary: str
    muted: str
    grid: str
    baseline: str
    series: tuple[str, ...]


LIGHT = Theme("light", "#fcfcfb", "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", ("#2a78d6", "#eb6834"))
DARK = Theme("dark", "#1a1a19", "#f0efec", "#c3c2b7", "#898781", "#2c2c2a", "#383835", ("#3987e5", "#d95926"))


def _font() -> str:
    from matplotlib import font_manager

    available = {f.name for f in font_manager.fontManager.ttflist}
    for name in FONT_CANDIDATES:
        if name in available:
            return name
    raise RuntimeError(f"日本語フォントが見つかりません：{FONT_CANDIDATES}")


def _frame(theme: Theme, title: str, attribution: str):
    plt.rcParams["font.family"] = _font()
    fig, ax = plt.subplots(figsize=(9.6, 5.4), dpi=150)
    fig.patch.set_facecolor(theme.surface)
    ax.set_facecolor(theme.surface)
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.spines["left"].set_color(theme.baseline)
    ax.spines["bottom"].set_color(theme.baseline)
    ax.tick_params(colors=theme.muted, labelsize=10, length=0)
    ax.set_title(title, loc="left", color=theme.ink, fontsize=15, fontweight="bold", pad=16)
    fig.text(0.01, 0.01, attribution, fontsize=7.5, color=theme.muted, ha="left", va="bottom")
    return fig, ax


def cumulative(stars: pd.DataFrame, theme: Theme):
    """O-01 距離ごとの、知られている星の数（累積）と、出来事ごとの到達半径"""
    fig, ax = _frame(theme, "地球からの距離と、その内側にある星の数", ATTRIBUTION_STARS)
    distances = (stars["dist"] * PC_TO_LY).sort_values().to_numpy()
    distances = distances[distances <= 115]
    ax.step(distances, range(1, len(distances) + 1), where="post", color=theme.series[0], linewidth=2)
    ax.grid(axis="y", color=theme.grid, linewidth=1)
    ax.set_axisbelow(True)
    ax.set_xlim(0, 115)
    ax.set_ylim(0, None)
    ax.set_xlabel("地球からの距離（光年）", color=theme.ink_secondary, fontsize=10)
    ax.set_ylabel("その距離までにある星の数（累積）", color=theme.ink_secondary, fontsize=10)
    top = ax.get_ylim()[1]
    for i, event in enumerate(EVENTS):
        r = reach_ly(event.date, REFERENCE_DATE)
        n = stars_within(stars, r)
        ax.axvline(r, color=theme.muted, linewidth=1)
        ax.plot([r], [n], marker="o", markersize=6, color=theme.series[0], markeredgecolor=theme.surface, markeredgewidth=1.5)
        y = top * (0.95 - 0.09 * i)
        ax.annotate(
            f"{event.label}\n{r:.0f}光年・{n:,}個",
            (r, y),
            xytext=(-6, 0),
            textcoords="offset points",
            ha="right",
            va="top",
            fontsize=9,
            color=theme.ink_secondary,
        )
    fig.subplots_adjust(left=0.1, right=0.97, top=0.88, bottom=0.14)
    return fig


def by_event(stars: pd.DataFrame, planets: pd.DataFrame, theme: Theme):
    """O-02 出来事ごとの、範囲内の星の数と惑星系の数（目盛りが違うので 2 つに分ける）"""
    plt.rcParams["font.family"] = _font()
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.8), dpi=150, sharey=True)
    fig.patch.set_facecolor(theme.surface)
    labels = [e.label.replace("（", "\n（") for e in EVENTS]
    radii = [reach_ly(e.date, REFERENCE_DATE) for e in EVENTS]
    panels = [
        ("知られている星", [stars_within(stars, r) for r in radii], theme.series[0]),
        ("惑星が見つかっている星", [planets_within(planets, r)[0] for r in radii], theme.series[1]),
    ]
    for ax, (title, values, color) in zip(axes, panels, strict=True):
        ax.set_facecolor(theme.surface)
        bars = ax.barh(labels, values, color=color, height=0.55)
        ax.bar_label(bars, labels=[f"{v:,}個" for v in values], padding=4, fontsize=9, color=theme.ink_secondary)
        ax.set_title(title, loc="left", color=theme.ink, fontsize=11, pad=8)
        ax.set_xlim(0, max(values) * 1.3)
        ax.xaxis.set_visible(False)
        for side in ("top", "right", "bottom"):
            ax.spines[side].set_visible(False)
        ax.spines["left"].set_color(theme.baseline)
        ax.tick_params(colors=theme.ink_secondary, labelsize=9, length=0)
    axes[0].invert_yaxis()  # 縦軸を共有しているので、反転は 1 回だけ（年代の古い順に上から並べる）
    fig.suptitle("電波が届いた範囲にあるもの", x=0.01, ha="left", color=theme.ink, fontsize=15, fontweight="bold")
    fig.text(0.01, 0.01, f"{ATTRIBUTION_STARS}／{ATTRIBUTION_PLANETS}", fontsize=7.5, color=theme.muted, ha="left", va="bottom")
    fig.subplots_adjust(left=0.24, right=0.97, top=0.82, bottom=0.1, wspace=0.15)
    return fig


def nearest(stars: pd.DataFrame, theme: Theme, count: int = 12):
    """O-03 太陽に近い恒星（ケンタウルス座α星系の 3 つを強調）"""
    fig, ax = _frame(theme, "太陽に近い星たち", ATTRIBUTION_STARS)
    ax.set_title("太陽に近い星たち", loc="left", color=theme.ink, fontsize=15, fontweight="bold", pad=34)  # 凡例の上に置く
    near = stars.sort_values(["dist", "id"], kind="mergesort").head(count)  # 距離が同じ星（α星 A・B）も毎回同じ順に
    names = [STAR_NAMES_JA.get(r["proper"] if isinstance(r["proper"], str) else r["gl"], r["gl"]) for _, r in near.iterrows()]
    colors = [theme.series[1] if r["proper"] in ALPHA_CEN else theme.series[0] for _, r in near.iterrows()]
    values = (near["dist"] * PC_TO_LY).to_numpy()
    bars = ax.barh(names, values, color=colors, height=0.6)
    ax.bar_label(bars, labels=[f"{v:.2f}光年" for v in values], padding=4, fontsize=9, color=theme.ink_secondary)
    ax.invert_yaxis()
    ax.set_xlim(0, values.max() * 1.18)
    ax.xaxis.set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.tick_params(colors=theme.ink_secondary, labelsize=9.5)
    from matplotlib.patches import Patch

    legend = ax.legend(
        handles=[
            Patch(color=theme.series[1], label="ケンタウルス座α星系（『三体』の舞台のモデル）"),
            Patch(color=theme.series[0], label="そのほかの星"),
        ],
        loc="lower left",
        bbox_to_anchor=(0, 1.0),
        ncol=2,
        frameon=False,
        fontsize=9,
        borderaxespad=0.3,
    )
    for text in legend.get_texts():
        text.set_color(theme.ink_secondary)
    fig.subplots_adjust(left=0.22, right=0.97, top=0.82, bottom=0.08)
    return fig


FIGURES = (
    ("O-01", "o01-cumulative-stars", "地球からの距離と、その内側にある星の数"),
    ("O-02", "o02-by-event", "電波が届いた範囲にあるもの"),
    ("O-03", "o03-nearest-stars", "太陽に近い星たち"),
)


def render_all(stars: pd.DataFrame, planets: pd.DataFrame) -> list[str]:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    written = []
    for theme in (LIGHT, DARK):
        drawn = {
            "O-01": cumulative(stars, theme),
            "O-02": by_event(stars, planets, theme),
            "O-03": nearest(stars, theme),
        }
        for fid, file, _ in FIGURES:
            name = f"{file}-{theme.name}.png"
            drawn[fid].savefig(FIGURES_DIR / name, facecolor=theme.surface, metadata={"Software": None})
            plt.close(drawn[fid])
            written.append(name)
    return written
