#!/usr/bin/python
# -*- coding: utf-8 -*-


import json
import requests

# id & secure key for access
#   format of id.json:
#{
#	"keyId":"xxxxxx" ,
#	"deviceId":"yyyyyyy" , 
#	"secretKey":"zzzzzzzzzzz"
#}

idFile='./id.json'

try:
    f=open(idFile, 'r')
except IOError:
    print 'No id.json file found!'
else:
    id=json.load(f)
    f.close()

    headers = {
        'x-device-secret': id['secretKey'] ,
        'Content-Type': 'application/json'
    }

    url = 'https://api.soracom.io/v1/devices/' + id['deviceId'] + '/publish'
 
    data = {'temp':36}

    response = requests.post(url , headers=headers, data=json.dumps(data))
