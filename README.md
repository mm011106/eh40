# eh40
このリポジトリはEH-40のデータロガーのためのソフトウエアです。

## 目標：
- BME280とADS1115の両方を同時にハンドリングできるスクリプトを組む
- それぞれのデバイスの基本的ハンドリングはそれぞれのライブラリに独立させる
- さらにSoracomでの通信が可能なようにする（雛形はすでにあり）

## 現状：
- BME280はそれなりに出来上がった
- ADS1115について、現在作成中
  - リードファンクションに計測完了のウエイトを入れる
- 参考URL　https://github.com/ControlEverythingCommunity/ADS1115/blob/master/Python/ADS1115.py
- 参考URL　https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15/blob/master/adafruit_ads1x15/ads1x15.py
  
