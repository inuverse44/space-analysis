"""地球の電波はどの星まで届いたか（docs/analysis-plan.md）。"""

import sys


def main(argv: list[str] | None = None) -> int:
    """`space-analysis`：検証 → 集計 → 図と表 → REPORT.md。`space-analysis fetch`：元データを取り込み直す"""
    args = sys.argv[1:] if argv is None else argv
    if args[:1] == ["fetch"]:
        from .fetch import fetch

        fetch()
        print("取得しました（data/raw/SOURCES.md を確認してください）")
        return 0

    from . import figures, report, summary
    from .load import load_planets, load_stars

    stars, planets = load_stars(), load_planets()  # V-01
    frames = summary.build(stars, planets)
    summary.write(frames)
    written = figures.render_all(stars, planets)
    report.write(frames)
    print(f"図 {len(written)} 枚・表 {len(frames)} 個・REPORT.md を作りました")
    return 0
