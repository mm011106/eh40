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

## update!
- ADS1115のドライブ用ライブラリが完成　2019/3/30

## ADS1115ドライバ
- 基本ファンクション
	- ADS.init(bus, address) : デフォルト設定でイニシャライズ。一度測定する。
	- ADS.readoutMulti(bus, address, readout_channels[] ) : 複数の（指定）チャネルを測定する。計測結果はリストで帰ってくる

#### ADS1115 データシート
https://cdn-shop.adafruit.com/datasheets/ads1115.pdf

## BME280 ドライバ
- 基本ファンクション
	- BME280.setup(bus, address) : イニシャライズ。
	- BME280.readData(bus, address) : 測定、リストが帰ってくる（温度、気圧、湿度）。


## 自動起動のためのサービス設定ファイル
- `/lib/systemd/system/サービス名.service`
- `sudo systemctl status サービス名.service` で確認
- `sudo systemctl stop|start サービス名.service`で、手動で 停止｜起動


## 動作確認例
```
$ sudo systemctl status soracom.service
● soracom.service - Soracom IoT edge device
   Loaded: loaded (/lib/systemd/system/soracom.service; enabled; vendor preset:
   Active: active (running) since Sun 2019-03-31 02:39:17 BST; 5min ago
 Main PID: 222 (python2.7)
   CGroup: /system.slice/soracom.service
           └─222 /usr/bin/python2.7 /home/pi/documents/eh40/soracom_ADC.py

Mar 31 02:39:17 raspberrypi systemd[1]: Started Soracom IoT edge device.
```

[systemctl](https://qiita.com/sinsengumi/items/24d726ec6c761fc75cc9)コマンドについて
