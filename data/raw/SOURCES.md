# 元データの記録（D-01、D-02、V-01）

| ファイル | 取得元 | 取得日 | 内容 | SHA-256 |
| --- | --- | --- | --- | --- |
| `hyg_v44_within40pc.csv` | https://codeberg.org/astronexus/hyg/media/branch/main/data/hyg/CURRENT/hyg_v44.csv.gz | 2026-10-11 | 元ファイル（SHA-256：`00b349893b9a53106dd488d8371e8d2fa586043e500bb3cdb8bff3931682197d`）から、距離 40 パーセク以下の行だけを抜き出したもの（列はそのまま） | `a55bb8233682804a20bb09a163f317c9a6016ea0ea78a335d4d2c7009f8eaef6` |
| `exoplanets_within40pc.csv` | https://exoplanetarchive.ipac.caltech.edu/TAP/sync | 2026-10-11 | 問い合わせ：`select pl_name,hostname,sy_dist,sy_snum,sy_pnum,pl_rade,pl_bmasse,pl_orbper,pl_orbsmax,disc_year,discoverymethod from pscomppars where sy_dist <= 40.0 order by sy_dist,pl_name` | `51c034585f98ecef8e6cba0294a865c4705666fd2fd5490294666e88b481b9f3` |

HYG Database は CC BY-SA 4.0。抜き出したファイルも同じライセンスで公開する。
