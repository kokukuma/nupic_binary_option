opf_experiment2
---

## パラメータを変更したいくつのモデルを作成
### n23-model
+ encoder
  + type: scalar
  + n: 23
  + w: 21

### n1000-model
+ encoder
  + type: scalar
  + n: 1000
  + w: 21

### delta-encoder-model
+ encoder : delta

### reset実行



## 結果


## 考察
+ なぜ, n23-modelにおいて, 予測値が実測値の3,4step前のとなってしまうのか.
+ なぜ, n1000-modelにおいて, 予測値が3つくらいの間でばらついてしまうのか. 
+ deltaによる影響.


