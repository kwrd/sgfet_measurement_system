## waveforms sdk

### レシーバーのコード

#### 設定する値

Time(グラフの時間の)
- Position : [ms]
- Base : [us/div]


Options
- Offset: [V]
- Ramge: [mV/div]


トリガー条件:
- 参考(http://daisan-y.private.coocan.jp/homepage/html/2019060401.html)
- 公式(https://reference.digilentinc.com/reference/software/waveforms/waveforms-3/reference-manual#triggers)


waveforms sdkで制御する内容
- spotの数のみで良いのでは?


### 送信側

- Type(square or sine)
- Frequency: 周波数(hz) (100kHz~10MHz)
  - 100k, 200k, 500k, 1M, 2M, 5M,10M
  - 
- Period: 振幅(second) 
- Amplitude(交流の振幅)(voltage) (1V, 2V, 5V)
- Offset(voltage) (-0.8, 1.6V)


## そもそも実験方法

### 送信側
- 先端Pt 
- 

### 受信側
- 先端 SGFET




### パスワード


1513



### 
とりが
- 立ち上がりのあるやつだけを取得
- 立ち下がりも可能


- 両方だと班は超ずれた波形も出てくる



オシロが写真を撮る時間
- とりがで決まる
  - 立ち上がりの時に写真を撮る




### acq hz 

#### 1秒間に取るサンプル数

##### 

10MHz 取る時,

撮りたい周波数の最低１０倍くらい



### 座標系の変換について

https://matplotlib.org/3.3.3/tutorials/advanced/transforms_tutorial.html



### 取得周波数について

waveform では Rate(acqHz)に応じて、画面の表示が変わる
- サンプルレートは大きい方がいいが、処理が重くなり意味がないので、下げていい、結果的にwaveform の使用でサンプリングレートが自動的に下げられている



### サンプリングレートについて
- https://www.edaq.com/wiki/Basics_of_Data_Acquisition
- 入力波形の周波数の最低二倍はサンプリングレートが必要



### AnalogTrg のやつ
msのやつ