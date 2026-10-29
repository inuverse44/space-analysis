"""D-01、D-02 の読み込みと検証（V-01）。"""

import pandas as pd

from .fetch import sha256_of
from .sources import EXO_FILE, HYG_SUBSET, SOURCES_MD


class DataValidationError(Exception):
    pass


def recorded_sha256(file_name: str) -> str:
    for line in SOURCES_MD.read_text(encoding="utf-8").splitlines():
        if line.startswith(f"| `{file_name}`"):
            return line.rstrip(" |").rsplit("`", 2)[-2]
    raise DataValidationError(f"{SOURCES_MD} に {file_name} の記録がありません")


def _verify(path) -> None:
    actual, expected = sha256_of(path), recorded_sha256(path.name)
    if actual != expected:  # V-01
        raise DataValidationError(f"{path.name} の SHA-256 が記録と一致しません：{actual} != {expected}")


def load_stars(verify: bool = True) -> pd.DataFrame:
    """恒星（距離はパーセク）。太陽（距離 0）と距離不明は除く"""
    if verify:
        _verify(HYG_SUBSET)
    df = pd.read_csv(HYG_SUBSET, dtype={"proper": str, "gl": str, "bayer": str, "con": str, "spect": str})
    df = df[(df["dist"] > 0) & (df["dist"] < 100000)].copy()
    return df


def load_sun() -> pd.Series:
    df = pd.read_csv(HYG_SUBSET, dtype={"proper": str, "spect": str})
    return df[df["proper"] == "Sol"].iloc[0]


def load_planets(verify: bool = True) -> pd.DataFrame:
    if verify:
        _verify(EXO_FILE)
    return pd.read_csv(EXO_FILE)
