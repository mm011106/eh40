#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import requests

# id & secure key for access
idFile='./id.json'

f=open(idFile, 'r')
id=json.load(f)
f.close()

headers = {
    'x-device-secret': id['secretKey'] ,
    'Content-Type': 'application/json'
}

url = 'https://api.soracom.io/v1/devices/' + id['deviceId'] + '/publish'

data = {'temp':36}

response = requests.post(url , headers=headers, data=json.dumps(data))
