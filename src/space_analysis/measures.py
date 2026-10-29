"""手法（docs/analysis-plan.md §4：M-01〜M-03）。"""

from datetime import date

import pandas as pd

from .sources import PC_TO_LY

JULIAN_YEAR_DAYS = 365.25


def reach_ly(since: date, until: date) -> float:
    """M-01 出来事の日から基準日までに、光が進んだ距離（光年）"""
    return (until - since).days / JULIAN_YEAR_DAYS


def stars_within(stars: pd.DataFrame, radius_ly: float) -> int:
    """M-02 太陽からの距離が radius_ly 以下の恒星の数"""
    return int((stars["dist"] * PC_TO_LY <= radius_ly).sum())


def planets_within(planets: pd.DataFrame, radius_ly: float) -> tuple[int, int]:
    """M-03 範囲内の惑星系（恒星）の数と、惑星の数"""
    inside = planets[planets["sy_dist"] * PC_TO_LY <= radius_ly]
    return int(inside["hostname"].nunique()), int(len(inside))
