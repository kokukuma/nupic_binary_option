opf_code_reading
---

## OPFの実装確認
### CLAモデル
+ 概要
  + nupic/frameworks/opf/clamodel.py
  + ここがモデルの中心. ここからをspとかtpとかを呼び出し利用する.
+ createCLANetworkがモデルの作成
  + Netowrokオブジェクトに, sensor, sp, tp, classifierを設定する.
  + sensor -> sp -> tp -> classifierの順で構成される.
  + HTMの考え方では, sp/tpで１つの層と見なしていたが, 実装上は異なる層と見立てられている.
  + なぜか, Netowrokの中身はC++で書かれる.
+ run
  + モデルの実行.
  + CLAは基本オンライン学習なので, learnみたいなというメソッドはない.
  + sensorの計算, spの計算, tpの計算をそれぞれ呼び出す.
  + tpの出力から, 分類やinputを再現する方法として, ReconstructionModel/ClassificationModel が残っているが, これはもう使われていない. multiStepModelに統一されたもよう.
  + 設定されたstep数先のinputを予測結果として返す.


### sensor (encoder)
+ 概要
  + nupic/encoders/multi.py
  + nupic/encoders/scalar.py
  + nupic/encoders/delta.py
  + 入力値をencodeして, SPに入力できるバイナリ列に変換する.

+ 役割
  + encoderの役割は２つ. 入力値のencodeとbucket_idの作成.
  + 入力値のencodeは辞書の形で渡された入力をバイナリ列に変換する.
  + int, float, category, 各種入力をバイナリ列に変換する. 
  + bucket_id は, classifierで使われるバイナリ列に対応する番号.

+ 重要なパラメータ
  + configで指定するパラメータに, n, wがある. 
  + nはencode後のバイナリ列の長さ. wはencode後アクティブになる数. 
  + 例えば, n=3/w=1なら, 100, 010, 001がバイナリ列として割り当てられる感じ. 
  + 入力の種類に対して, n/wで作られるバイナリ列の数が少ないと, 多くの入力が同じバイナリ列で表現されることになり上手く予測できなくなる.


### spacial pooler
+ 概要
  + nupic/region/research/spatial_pooler.py
  + encoderから渡されたバイナリ列を疎分散表現(SDR)に変換する.
  + どのカラムが発火するかを決める.
+ ホワイトペーパーと同じと考えてよいだろう.


### temporal pooler
+ 概要
  + nupic/region/research/TP.py
  + spから渡されたSDRをもとに, カラム中のどのセルが発火しているかを決める.
+ ホワイトペーパーと同じと考えてよいだろう.


### cla classifier
+ 概要
  + nupic/algorithms/CLAClassifier.py
  + tpで得られたセルの発火状況から, 元の入力を予測する.

+ 予測方法
  + あるセルが発火した後, 次の入力が何であるかの確率を保存する.
  + これをもとに, あるセルが発火した次に, どの入力がくるかを予測する.
  + これを, 発火している全てのセルに対して行い, 次に来る入力を予測する.

+ データの保存
  + あるセルが発火した後, 次の入力が何であるかの確率を保存する.
  + BitHistoryのインスタンスにデータが保存される. 入力に対する確率のテーブルをイメージするとよい.
  + この BitHistoryが, セル/予測ステップ数分だけ用意される.
  + CLAClassifierが, それまで入力された全ての入力とそのとき得られたセルの発火パターンを記憶しておく.
  + これをもとに, ある入力の設定ステップ前の発火パターンを使い, BitHistoryにデータを貯める.
  + セルが発火していない場合, BitHistoryにデータは追加されない.

+ bucket_id 
  + 入力は直接使われるのではなく, bucket_idに直して使われる.
    + 入力がカテゴリ変数の場合, テーブルはカテゴリ変数に対する確率で良いが, 入力が実数の場合困ってしまうので.
  + このbucekt_idを出すために, encoderが使われる. 
  + 入力が実数の場合は, bucekt_idに対する実際の入力値は, 今まで入力された値をもとに, 徐々に更新されていく.
  + そのため, BitHistory毎に, bucket_idに対する実際の入力値は異なる.


## 重要なパラメータまとめ
+ inferenceType
  + TemporalAnomaly

+ sensorParams/encoder
  + encoderの設定に必要なパラメータ.
  + 入出力の分だけ設定する.
  + ScalarEncoder/DeltaEncoder以外では, 必要なパラメータがまた変わってくる.

  | param          |                                                |
  | -------        | --------------                                 |
  | fieldname      | フィールド名                                   |
  | maxval         | 値が取りうるmax値. 超えると, maxvalが使われる. |
  | minval         | 値が取りうるmin値. 超えると, minvalが使われる. |
  | type           | encoderのtype.                                 |
  | n              | encode後のbin列の長さ.                         |
  | w              | encode後のbin列でactiveになる数(1の数).        |
  | classifierOnly | Trueにすると, 入力では使われない.              |
  | radius         | bin列間でどのくらい違いが出るかを指定.         |
  | resolution     | bin列間でどのくらい違いが出るかを指定.         |

+ spParams
  + spacial poolerの設定で必要なパラメータ.
  + 詳しくは, nupic/region/research/spatial_pooler.py を参照.

  | param                      |                                                           |
  | -------                    | --------------                                            |
  | columnCount                | カラム数                                                  |
  | inputWidth                 | encoderのnに調整される.                                   |
  | numActiveColumnsPerInhArea | 一つの表現で発火するカラム数(基本, columnCountの2%が推奨) |
  | potentialPct               | encoderから渡されたinputを利用する割合. 1.0なら全結合.    |
  | maxBoost                   | ブースト値                                                |
  | globalInhibition           | ?                                                         |
  | synPermActiveInc           | ?                                                         |
  | synPermConnected           | ?                                                         |
  | synPermInactiveDec         | ?                                                         |


+ tpParams
  + temporal poolerの設定で必要なパラメータ.
  + 詳しくは, nupic/region/research/TP.py を参照.

  | cellsPerColumn        | １カラムに含まれるセル数                                                      |
  | columnCount           | SPのカラム数と同じものを.                                                     |
  | inputWidth            | columnCountと同じものを.                                                      |
  | outputType            | normalでは, active+predict. activeStateではactiveのみ. activeState1CellPerCol |
  | activationThreshold   | ?                                                                             |
  | globalDecay           | ?                                                                             |
  | initialPerm           | ?                                                                             |
  | maxAge                | ?                                                                             |
  | maxSegmentsPerCell    | ?                                                                             |
  | maxSynapsesPerSegment | ?                                                                             |
  | minThreshold          | ?                                                                             |
  | newSynapseCount       | ?                                                                             |
  | pamLength             | ?                                                                             |
  | burnIn                | ?                                                                             |
  | connectedPerm         | ?                                                                             |
  | permanenceDec         | ?                                                                             |
  | permanenceInc         | ?                                                                             |


