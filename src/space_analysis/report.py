"""O-06 REPORT.md を作る。数値は毎回データから埋める。"""

import pandas as pd

from .figures import FIGURES
from .sources import ATTRIBUTION_STARS, REFERENCE_DATE, ROOT

METHODS_JA = {"Radial Velocity": "視線速度法", "Transit": "トランジット法", "Imaging": "直接撮像", "Microlensing": "重力マイクロレンズ法"}


def _luminosity(value: float) -> str:
    """明るさ（太陽＝1）。とても暗い星は「約 N 分の 1」と書く"""
    return f"{value:.2f}" if value >= 0.01 else f"約 {1 / value:,.0f} 分の 1"


def _picture(file: str, alt: str) -> str:
    return (
        "<picture>\n"
        f'  <source media="(prefers-color-scheme: dark)" srcset="figures/{file}-dark.png">\n'
        f'  <img src="figures/{file}-light.png" alt="{alt}" width="100%">\n'
        "</picture>"
    )


def render(frames: dict[str, pd.DataFrame]) -> str:
    reach = frames["reach_by_event.csv"].set_index("event_id")
    alpha = frames["alpha_centauri.csv"]
    proxima = frames["proxima_planets.csv"]
    fig = {fid: (file, title) for fid, file, title in FIGURES}
    radio, tv, apollo, arecibo = (reach.loc[i] for i in ("E-01", "E-02", "E-03", "E-04"))
    alpha_dist = alpha[alpha["name"] == "ケンタウルス座α星A"]["distance_ly"].iloc[0]
    proxima_lum = alpha[alpha["name"] == "プロキシマ・ケンタウリ"]["luminosity_sun"].iloc[0]
    b = proxima[proxima["pl_name"] == "Proxima Cen b"].iloc[0]

    reach_rows = "\n".join(
        f"| {r['event']} | {r['reach_ly']:.0f} 光年 | {r['known_stars']:,} 個 | {r['planet_systems']:,} 個（惑星 {r['planets']:,} 個） |"
        for _, r in frames["reach_by_event.csv"].iterrows()
    )
    alpha_rows = "\n".join(
        f"| {r['name']} | {r['spectral_type']} | {r['distance_ly']:.2f} 光年 | {_luminosity(r['luminosity_sun'])} |"
        for _, r in alpha.iterrows()
    )
    planet_rows = "\n".join(
        f"| {r['pl_name']} | 地球の約 {r['pl_bmasse']:.2f} 倍 | {r['pl_orbper']:.1f} 日 | {r['pl_orbsmax']:.3f} 天文単位 | {r['disc_year']} 年（{METHODS_JA.get(r['discoverymethod'], r['discoverymethod'])}） |"
        for _, r in proxima.iterrows()
    )

    return f"""# 地球の電波は、どの星まで届いたか ―『三体』になぞらえて

SF 小説『三体』では、地球から出た電波が別の星系に届くところから物語が動き出します。現実の地球も、100 年ほど前からラジオやテレビの電波を宇宙に出し続けています。その電波がいまどこまで届いていて、そこにどんな星があるのかを、公開データで数えてみました。

基準日は {REFERENCE_DATE.year} 年 {REFERENCE_DATE.month} 月 {REFERENCE_DATE.day} 日です。分析の進め方は [分析計画書](docs/analysis-plan.md) に、計算はすべて [src/](src/) にあります。

## 要点

- 1920 年に始まったラジオの定時放送の電波は、いま地球から約 **{radio["reach_ly"]:.0f} 光年** の球の内側まで届いています。その中には、知られている星が **{radio["known_stars"]:,} 個**あり、そのうち **{radio["planet_systems"]:,} 個** では惑星が見つかっています。
- 1969 年のアポロ 11 号の月面中継は約 {apollo["reach_ly"]:.0f} 光年先まで進み、{apollo["known_stars"]:,} 個の星を通り過ぎました。
- 『三体』の舞台のモデルになったケンタウルス座α星系までは約 {alpha_dist:.1f} 光年です。1974 年のアレシボ・メッセージ（約 {arecibo["reach_ly"]:.0f} 光年先まで進んでいる）なら、この星系と地球の間を **{arecibo["reach_ly"] / (2 * alpha_dist):.0f} 往復** できるほどの時間がたっています。

## Q-01 地球の電波は、いまどこまで届いていて、その中に星はいくつあるか

{_picture(*fig["O-01"])}

電波は光と同じ速さで進むので、出来事の日から基準日までの年数が、そのまま「届いた半径（光年）」になります。

| 出来事 | 届いた半径 | 範囲内の知られている星 | 惑星が見つかっている星 |
| --- | --- | --- | --- |
{reach_rows}

- 半径が 2 倍になると、球の体積は 8 倍になります。そのため、届いた範囲が広がるほど、内側にある星の数は急に増えていきます。

## Q-02 電波が届いた範囲に、惑星が見つかっている星はいくつあるか

{_picture(*fig["O-02"])}

- ベルリン五輪のテレビ中継（約 {tv["reach_ly"]:.0f} 光年）の範囲だけでも、惑星が見つかっている星が {tv["planet_systems"]:,} 個、惑星が {tv["planets"]:,} 個あります。

## Q-03 『三体』の舞台のモデル、ケンタウルス座α星系

{_picture(*fig["O-03"])}

ケンタウルス座α星系は、太陽に一番近い恒星系です。3 つの星からなり、小説の「三体」のモデルになりました。

| 星 | スペクトル型 | 距離 | 明るさ（太陽＝1） |
| --- | --- | --- | --- |
{alpha_rows}

- α星 A は太陽とよく似た星（スペクトル型 G2）で、明るさは太陽の約 {alpha.iloc[1]["luminosity_sun"]:.1f} 倍です。
- プロキシマ・ケンタウリは小さな赤色矮星で、明るさは太陽の約 {1 / proxima_lum:,.0f} 分の 1 しかありません。

プロキシマ・ケンタウリには、惑星が見つかっています。

| 惑星 | 質量 | 公転周期 | 恒星からの距離 | 発見 |
| --- | --- | --- | --- | --- |
{planet_rows}

- プロキシマ b は、地球と同じくらいの質量の惑星が {b["pl_orbper"]:.1f} 日で恒星の周りを回っています。質量は、恒星のふらつきから求めた推定値です。

## このデータの限界

- **星の数は「知られている星」の数です。** HYG Database は明るい星と、よく知られた近くの星を網羅していますが、暗い赤色矮星や褐色矮星の多くは入っていません。実際の星の数は、これより多くなります。
- **「届いた」は、光の速さで計算した理論上の範囲です。** 遠くに届いた電波はとても弱くなるので、受信できる強さかどうかは、この分析では扱っていません。
- 星の距離はカタログの値で、誤差があります。範囲の境目にある星は、数に入るかどうかが変わることがあります。

## 再現の手順

```sh
uv sync
uv run space-analysis     # 検証 → 集計 → 図と表 → このレポート
uv run pytest
```

---

- {ATTRIBUTION_STARS}。加工したデータ（`data/`）と図（`figures/`）も CC BY-SA 4.0 です。
- This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.（Christiansen et al. 2025, Planetary Science Journal, doi:10.3847/PSJ/ade3c2）
- 小説『三体』（劉慈欣）の本文や画像は使っていません。
"""


def write(frames: dict[str, pd.DataFrame]) -> None:
    (ROOT / "REPORT.md").write_text(render(frames), encoding="utf-8")
