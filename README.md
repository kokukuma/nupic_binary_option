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


## 実験１
+ データ
  + 2002-2005の時間単位のヒストリカルデータ(high/low)
+ 結果
  + swarmm
    + 時間長過ぎ. モデル作るのに6時間くらいかかった.
  + 予測
    + 2, 3年の時は, 急激に予測値がずれることとかあった.
    + 5年目後半になるとそれもなくなり落ち着いている.
    + しかし, 予測値は実測より一歩遅れている感が否めない.
    + また, binary optionの勝率も44 - 49%あたりを漂ってる.
+ 考察
  + そもそも, 予測する材料が足りているのか?
    + とりあえず, open/closeも予測に含めた方が良い.
      + http://www.nomura.co.jp/learn/chart/page8.html
    + 他の通貨との関連
    + 過去のニュース

## 実験２
  + データ
    + 2002-2005の時間単位のヒストリカルデータ(open/high/low/close)

## 実験３
  + データ
    + 2002-2005の日単位のヒストリカルデータ(open/high/low/close)

## 次にやること
+ 区切り位置の検討(1日, 数時間)
+ 学習に関して
  + １ヶ月分を11回くらい学習させたら, 結果は改善するだろうか?
  + 5年分学習させた後, 1年分予測.


## OPFについて
+ saveメソッドで, 学習した内容保存されている?.
+ 2パラメータを予測するには? 





