# 地球の電波は、どの星まで届いたか ―『三体』になぞらえて

公開データを使ったデータ解析の見本その 2 です。地球が 100 年ほど前から出し続けているラジオやテレビの電波が、いまどこまで届いていて、そこにどんな星があるのかを、公開データ（恒星カタログと NASA の系外惑星アーカイブ）で数えました。

- 結果：[REPORT.md](REPORT.md)
- 分析計画書（問い・データ・手法・検証・トレーサビリティ）：[docs/analysis-plan.md](docs/analysis-plan.md)
- ホームページ：https://www.inuverse.dev
- 見本その 1：[消費者物価指数で見る、物価とお米](https://github.com/inuverse44/cpi-analysis)

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="figures/o02-by-event-dark.png">
  <img src="figures/o02-by-event-light.png" alt="電波が届いた範囲にあるもの" width="100%">
</picture>

## 再現の手順

```sh
uv sync
uv run space-analysis          # 検証 → 集計 → 図と表 → REPORT.md
uv run pytest                  # 検証（分析計画書 §6）
uv run space-analysis fetch    # 元データを取り込み直す（SOURCES.md も更新）
```

## 出典とライセンス

- 星のデータ：HYG Database v4.4（astronexus、CC BY-SA 4.0）を加工。`data/` と `figures/` は **CC BY-SA 4.0** です。
- 惑星のデータ：This research has made use of the NASA Exoplanet Archive, which is operated by the California Institute of Technology, under contract with the National Aeronautics and Space Administration under the Exoplanet Exploration Program.（Christiansen et al. 2025, PSJ, doi:10.3847/PSJ/ade3c2）
- コード（`src/`、`tests/`、`scripts/`）：MIT License
- 小説『三体』（劉慈欣）の本文や画像は使っていません。
