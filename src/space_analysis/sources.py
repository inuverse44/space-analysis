"""データの出所と定数（docs/analysis-plan.md §3、§4）。"""

from dataclasses import dataclass
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
PROCESSED_DIR = ROOT / "data" / "processed"
FIGURES_DIR = ROOT / "figures"
SOURCES_MD = RAW_DIR / "SOURCES.md"

# D-01 HYG Database v4.4（CC BY-SA 4.0）。元ファイルは大きいので、近い星だけを抜き出して保存する
HYG_URL = "https://codeberg.org/astronexus/hyg/media/branch/main/data/hyg/CURRENT/hyg_v44.csv.gz"
HYG_SUBSET = RAW_DIR / "hyg_v44_within40pc.csv"
SUBSET_MAX_PC = 40.0

# D-02 NASA Exoplanet Archive（Planetary Systems Composite Parameters）
EXO_QUERY = (
    "select pl_name,hostname,sy_dist,sy_snum,sy_pnum,pl_rade,pl_bmasse,pl_orbper,pl_orbsmax,disc_year,discoverymethod "
    f"from pscomppars where sy_dist <= {SUBSET_MAX_PC} order by sy_dist,pl_name"
)
EXO_URL = "https://exoplanetarchive.ipac.caltech.edu/TAP/sync"
EXO_FILE = RAW_DIR / "exoplanets_within40pc.csv"

PC_TO_LY = 3.261563777  # 1 パーセク = 3.2616 光年（IAU）

# 基準日：データを取得した日（M-01）
REFERENCE_DATE = date(2026, 10, 11)


@dataclass(frozen=True)
class Event:
    id: str
    label: str
    date: date


# E-01〜E-04
EVENTS: tuple[Event, ...] = (
    Event("E-01", "ラジオの定時放送（KDKA、1920年）", date(1920, 11, 2)),
    Event("E-02", "ベルリン五輪のテレビ中継（1936年）", date(1936, 8, 1)),
    Event("E-03", "アポロ11号の月面中継（1969年）", date(1969, 7, 21)),
    Event("E-04", "アレシボ・メッセージ（1974年）", date(1974, 11, 16)),
)

ATTRIBUTION_STARS = "星：HYG Database v4.4（astronexus, CC BY-SA 4.0）を加工"
ATTRIBUTION_PLANETS = "惑星：NASA Exoplanet Archive"
