opf_binary_option
---

## モデル
### 実測値予想モデル
+ 入力: low_valueの差分
+ 出力: low_valueの差分

+ encoder
  + type: scalar
  + n: 1000
  + w: 21
+ reset : 10 step毎


### high/low直接予想モデル
+ 入力: open, close, high, low
+ 出力: low_value, low_value_delta, high_low

+ encoder
  + type: delta
  + n: 1000
  + w: 21
+ reset : 10 step毎



## 評価方法
+ 2001 - 2005年のヒストリカルデータを使い学習.
+ 2006 - 2007年のデータで結果を確認する.

## 結果
+ 2001- 2005 (保存してやってみる)
  + 30593 : 0.5506
  + 61186 : 0.6130
  + 91779 : 0.5839
+ 2006年(学習なし)
  + 0.6033


## 考察

