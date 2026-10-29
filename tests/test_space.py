"""検証（docs/analysis-plan.md §6）"""

from datetime import date

import pytest

from space_analysis.load import load_planets, load_stars
from space_analysis.measures import planets_within, reach_ly, stars_within
from space_analysis.sources import PC_TO_LY


@pytest.fixture(scope="module")
def stars():
    return load_stars()


@pytest.fixture(scope="module")
def planets():
    return load_planets()


def test_v01_raw_data_matches_recorded_sha256(stars, planets):
    assert len(stars) > 0 and len(planets) > 0  # 一致しなければ読み込みで DataValidationError


def test_v02_proxima_is_about_4_24_light_years(stars):
    proxima = stars[stars["proper"] == "Proxima Centauri"].iloc[0]
    assert 4.2 <= proxima["dist"] * PC_TO_LY <= 4.3


def test_v02_sun_is_not_counted(stars):
    assert "Sol" not in set(stars["proper"].dropna())


def test_v03_reach_matches_hand_calculation():
    assert reach_ly(date(2025, 1, 1), date(2026, 1, 1)) == pytest.approx(365 / 365.25)
    assert reach_ly(date(2000, 1, 1), date(2100, 1, 1)) == pytest.approx(100.0, abs=0.01)


def test_v04_counts_do_not_decrease_with_radius(stars, planets):
    radii = [5, 10, 20, 50, 90, 106, 130]
    star_counts = [stars_within(stars, r) for r in radii]
    planet_counts = [planets_within(planets, r)[0] for r in radii]
    assert star_counts == sorted(star_counts)
    assert planet_counts == sorted(planet_counts)


def test_v05_proxima_b_is_in_the_exoplanet_archive(planets):
    row = planets[planets["pl_name"] == "Proxima Cen b"].iloc[0]
    assert row["sy_dist"] == pytest.approx(1.30, abs=0.02)


def test_v06_committed_outputs_match_regenerated(stars, planets):
    """V-06：加工済みデータとレポートが、コードから毎回同じものとして作り直せる"""
    import io

    from space_analysis.report import render
    from space_analysis.sources import PROCESSED_DIR, ROOT
    from space_analysis.summary import build

    frames = build(stars, planets)
    for name, frame in frames.items():
        buffer = io.StringIO()
        frame.to_csv(buffer, index=False, lineterminator="\n")
        assert buffer.getvalue() == (PROCESSED_DIR / name).read_text(encoding="utf-8"), name
    assert render(frames) == (ROOT / "REPORT.md").read_text(encoding="utf-8")
