# eh40
このリポジトリはEH-40のデータロガーのためのソフトウエアです。

## 目標：
- BME280とADS1115の両方を同時にハンドリングできるスクリプトを組む
- それぞれのデバイスの基本的ハンドリングはそれぞれのライブラリに独立させる
- さらにSoracomでの通信が可能なようにする（雛形はすでにあり）

## 現状：
- 2019/06 リリースできる状態：NYU向けに4GB-SDに入れてリリース
- BME280はそれなりに出来上がった
- ADS1115について、現在作成中
  - リードファンクションに計測完了のウエイトを入れる
- 参考URL　https://github.com/ControlEverythingCommunity/ADS1115/blob/master/Python/ADS1115.py
- 参考URL　https://github.com/adafruit/Adafruit_CircuitPython_ADS1x15/blob/master/adafruit_ads1x15/ads1x15.py

## update!
- shutdown sw のハンドリングスクリプトを吸収しました。　2019/06/28
- ADS1115のドライブ用ライブラリが完成　2019/3/30
- ADS,BMEの両方を同時に読み取るように変更し、リリース版を作成  2019/4/7
  - EH-40のアンプ増幅率などを加味して、電圧をリードアウトするようにした
  - ADSは差動　0−1:液面, 2−3：圧力計　

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
- `/etc/systemd/system/サービス名.service`
- `sudo systemctl status サービス名.service` で確認
- `sudo systemctl stop|start サービス名.service`で、手動で 停止｜起動
- `sudo systemctl restart サービス名.service`で、変更したスクリプトを有効に
- `sudo systemctl daemon-reload`で、.serviceを変更した場合のアップデート

## 動作確認例
```
$ sudo systemctl status soracom.service
● soracom.service - Soracom IoT edge device
   Loaded: loaded (/etc/systemd/system/soracom.service; enabled; vendor preset:
   Active: active (running) since Sun 2019-03-31 02:39:17 BST; 5min ago
 Main PID: 222 (python2.7)
   CGroup: /system.slice/soracom.service
           └─222 /usr/bin/python2.7 /home/pi/documents/eh40/soracom_ADC.py

Mar 31 02:39:17 raspberrypi systemd[1]: Started Soracom IoT edge device.
```

[systemctl](https://qiita.com/sinsengumi/items/24d726ec6c761fc75cc9)コマンドについて

## Turn Off the swap file

`sudo systemctl stop dphys-swapfile.service`

`sudo systemctl disable dphys-swapfile.service`

このコマンドで設定の確認

`systemctl status dphys-swapfile.service`


# 設定ファイル
##　ppp設定

```
$ sudo ls -al /etc/ppp/peers/soracom_MS2372
-rw-r----- 1 root dip 299 Apr 13 09:13 /etc/ppp/peers/soracom_MS2372
```

## udev用ルールファイル

```
$ sudo ls -al /etc/udev/rules.d/40-MS2372.rules
-rw-r--r-- 1 root root 179 Apr 13 08:55 /etc/udev/rules.d/40-MS2372.rules
```

## ネットワークインターフェイス設定

```
$ sudo ls -al /etc/network/interfaces
-rw-r--r-- 1 root root 342 Apr 13 07:56 /etc/network/interfaces
```
に追加する。

## ppp接続用チャットスクリプト

```
$ sudo ls -al /etc/chatscripts/soracom_MS2372
-rw-r----- 1 root dip 494 Apr 13 02:16 /etc/chatscripts/soracom_MS2372
```


# Shutdown switch for RaspberryPi

## 機能
- RaspberryPiにシャットダウンスイッチの機能をつけます。
- スイッチを3秒程度押し続けると、シャットダウンコマンドが発行され、電源が切れます。

## 使うもの
- __GPIO 17__ プルアップ：　シャットダウンスイッチ入力　スイッチをこことGNDの間に接続します。
  - できれば、0.1uF程度のコンデンサをGNDに対して入れるといい。
- __GPIO 21__ ：シャットダウンプロセスが起動したことを示すLEDのための出力　アクティブHi

## ログファイル
- `/var/log/shutdwnSwitch.log`
- `sudo tailf /var/log/shutdwnSwitch.log` で表示すると動作確認に便利

## サービス設定ファイル
- `/lib/systemd/system/shutdwnSw.service`
- `sudo systemctl status shutdwnSw.service` で確認
- `sudo systemctl stop|start shutdwnSw.service`で、手動で 停止｜起動
- `sudo systemctl enable shutdwnSw.service`で、永続化
- `sudo systemctl daemon-reload`で、.serviceを変更した場合のアップデート


## 動作確認例
```
$ sudo systemctl status shutdwnSw.service
● shutdwnSw.service - Shutdown Switch watcher
   Loaded: loaded (/lib/systemd/system/shutdwnSw.service; enabled; vendor preset
   Active: active (running) since Sun 2019-03-31 02:39:17 BST; 5min ago
 Main PID: 215 (python2.7)
   CGroup: /system.slice/shutdwnSw.service
           └─215 /usr/bin/python2.7 /home/pi/documents/resetSW/shutdwnSwitch.py

Mar 31 02:39:17 raspberrypi systemd[1]: Started Shutdown Switch watcher.
```

[systemctl](https://qiita.com/sinsengumi/items/24d726ec6c761fc75cc9)コマンドについて
