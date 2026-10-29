"""データの取り込み（docs/analysis-plan.md §3）。取得日と SHA-256 を SOURCES.md に記録する（V-01）。"""

import gzip
import hashlib
import io
import urllib.parse
import urllib.request
from datetime import date

import pandas as pd

from .sources import EXO_FILE, EXO_QUERY, EXO_URL, HYG_SUBSET, HYG_URL, SOURCES_MD, SUBSET_MAX_PC


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_of(path) -> str:
    return sha256_bytes(path.read_bytes())


def _get(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "space-analysis (inuverse44)"})
    with urllib.request.urlopen(request, timeout=120) as response:  # 取得元は固定の https URL
        return response.read()


def fetch(today: date | None = None) -> None:
    today = today or date.today()
    RAW_DIR = HYG_SUBSET.parent
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    hyg_gz = _get(HYG_URL)
    hyg = pd.read_csv(io.BytesIO(gzip.decompress(hyg_gz)), dtype=str, keep_default_na=False)
    dist = pd.to_numeric(hyg["dist"], errors="coerce")
    subset = hyg[(dist <= SUBSET_MAX_PC)]  # 太陽（距離 0）も含めて保存し、数えるときに除く
    subset.to_csv(HYG_SUBSET, index=False, lineterminator="\n")

    exo = _get(f"{EXO_URL}?{urllib.parse.urlencode({'query': EXO_QUERY, 'format': 'csv'})}")
    EXO_FILE.write_bytes(exo)

    SOURCES_MD.write_text(
        "# 元データの記録（D-01、D-02、V-01）\n\n"
        "| ファイル | 取得元 | 取得日 | 内容 | SHA-256 |\n"
        "| --- | --- | --- | --- | --- |\n"
        f"| `{HYG_SUBSET.name}` | {HYG_URL} | {today.isoformat()} | 元ファイル（SHA-256：`{sha256_bytes(hyg_gz)}`）から、"
        f"距離 {SUBSET_MAX_PC:g} パーセク以下の行だけを抜き出したもの（列はそのまま） | `{sha256_of(HYG_SUBSET)}` |\n"
        f"| `{EXO_FILE.name}` | {EXO_URL} | {today.isoformat()} | 問い合わせ：`{EXO_QUERY}` | `{sha256_of(EXO_FILE)}` |\n\n"
        "HYG Database は CC BY-SA 4.0。抜き出したファイルも同じライセンスで公開する。\n",
        encoding="utf-8",
    )
