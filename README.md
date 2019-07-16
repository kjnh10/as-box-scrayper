# Usage

## 準備

* google chromeとchrome driverをダウンロードして入れておく。
  * google chromeのversionとchrome driverのversionを合わせておく。(75.03770.140でうまく回ることは確認済み)
  * chrome driverをPATHの通ったところにおいておく。

## 実行

* python as-box.pyを実行するとresults/の下に結果のファイルが生成される。
* デバッグする場合はoptions.add_argument('-headless')のコメントアウトを外すとブラウザが見えるようになる。
* 注意: たまに失敗する場合があるので落ちているケースがないか確認する必要あり。
