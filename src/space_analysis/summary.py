"""O-04 比較の表と O-05 加工済みデータ（docs/analysis-plan.md §5）。HYG を加工したものは CC BY-SA 4.0。"""

import pandas as pd

from .figures import ALPHA_CEN, STAR_NAMES_JA
from .load import load_sun
from .measures import planets_within, reach_ly, stars_within
from .sources import EVENTS, PC_TO_LY, PROCESSED_DIR, REFERENCE_DATE


def reach_by_event(stars: pd.DataFrame, planets: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for e in EVENTS:
        r = reach_ly(e.date, REFERENCE_DATE)
        systems, count = planets_within(planets, r)
        rows.append(
            {
                "event_id": e.id,
                "event": e.label,
                "date": e.date.isoformat(),
                "reach_ly": round(r, 2),
                "known_stars": stars_within(stars, r),
                "planet_systems": systems,
                "planets": count,
            }
        )
    return pd.DataFrame(rows)


def alpha_centauri(stars: pd.DataFrame) -> pd.DataFrame:
    sun = load_sun()
    rows = [{"name": "太陽", "spectral_type": sun["spect"], "distance_ly": 0.0, "luminosity_sun": 1.0}]
    for _, r in stars[stars["proper"].isin(ALPHA_CEN)].sort_values("lum", ascending=False).iterrows():
        rows.append(
            {
                "name": STAR_NAMES_JA[r["proper"]],
                "spectral_type": r["spect"],
                "distance_ly": round(r["dist"] * PC_TO_LY, 3),
                "luminosity_sun": float(f"{r['lum']:.3g}"),
            }
        )
    return pd.DataFrame(rows)


def proxima_planets(planets: pd.DataFrame) -> pd.DataFrame:
    p = planets[planets["hostname"] == "Proxima Cen"]
    return p[["pl_name", "pl_bmasse", "pl_orbper", "pl_orbsmax", "disc_year", "discoverymethod"]].reset_index(drop=True)


def nearest_stars(stars: pd.DataFrame, count: int = 12) -> pd.DataFrame:
    near = stars.sort_values(["dist", "id"], kind="mergesort").head(count)  # 距離が同じ星（α星 A・B）も毎回同じ順に
    return pd.DataFrame(
        {
            "name": [STAR_NAMES_JA.get(r["proper"] if isinstance(r["proper"], str) else r["gl"], r["gl"]) for _, r in near.iterrows()],
            "distance_ly": (near["dist"] * PC_TO_LY).round(3).to_numpy(),
            "spectral_type": near["spect"].to_numpy(),
        }
    )


def build(stars: pd.DataFrame, planets: pd.DataFrame) -> dict[str, pd.DataFrame]:
    return {
        "reach_by_event.csv": reach_by_event(stars, planets),
        "alpha_centauri.csv": alpha_centauri(stars),
        "proxima_planets.csv": proxima_planets(planets),
        "nearest_stars.csv": nearest_stars(stars),
    }


def write(frames: dict[str, pd.DataFrame]) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    for name, frame in frames.items():
        frame.to_csv(PROCESSED_DIR / name, index=False, lineterminator="\n")
