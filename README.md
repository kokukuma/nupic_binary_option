nupic_binary_option
---

## 目標
+ ヒストリカルデータにおいて1時間後のhigh/lowを予想する.


## 資料
+ バイナリオプションの基礎
  + http://xn--eckm3b6d2a9b3gua9f2d.com/appeal/

+ 過去のヒストリカルデータ
  + http://www.forextester.com/data/datasources.html

+ 取り扱い方
  + http://boatrader.ehoh.net/history_sort.html
  + http://fusa232323.blog.fc2.com/blog-entry-77.html


## とりあえずやってみる.
+ データ
  + 2002-2005の時間単位のヒストリカルデータ(high/low)
+ 結果
  + swarmm
    + 時間長過ぎ. モデル作るのに6時間くらいかかった.
    + できたモデル: 
  + 予測
    + 2, 3年の時は, 急激に予測値がずれることとかあった.
    + 5年目後半になるとそれもなくなり落ち着いている.
    + しかし, 予測値は実測より一歩遅れている感が否めない.
    + また, binary optionの勝率も44 - 49%あたりを漂ってる.
+ 思ったこと
  + そもそも, 予測する材料が足りているのか?
    + とりあえず, open/closeも予測に含めた方が良い.
      + http://www.nomura.co.jp/learn/chart/page8.html
    + 他の通貨との関連
    + 過去のニュース
  + パラメータは本当に正しい値になっているのか?


## 方向性の検討
+ 目標: 簡単なデータで, 正しく予測できるようなモデルを作成する.
1. [OPFの実装把握](docs/opf_code_reading.md)
  + 実装を確認
  + 重要なパラメータまとめ
1. [ベースモデル](docs/opf_experiment.md) 未
  + モデルのパラメータ確認
  + 結果, 考察
1. [パラメータ影響調査](docs/opf_experiment2.md) 未
  + 実装と途中経過の結果を確認し疑問を解消.
  + パラメータの結果に対する影響を把握する.

1. [予測をするためのモデル構築]()   未
  + high/low直接予測
  + 複数点トレンド予測. 
  + 2003-2005の時間単位のヒストリカルデータ(closeのみkk)
  + 2002-2005の時間単位のヒストリカルデータ(open/high/low/close)
  + 2002-2005の時間単位のヒストリカルデータ(open/high/low/close) max-min調整
  + 2002-2005の日単位のヒストリカルデータ(open/high/low/close)


## パラメータ


## OPFについて
+ saveメソッドで, 学習した内容保存されている?.
+ 2パラメータを予測するには? 





