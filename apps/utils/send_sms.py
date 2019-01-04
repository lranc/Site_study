# -*- coding:utf8 -*-

import requests
import time
import hashlib
import random
import json


class TenMessage():
    def __init__(self, AppID, AppKey):
        self.AppID = AppID
        self.AppKey = AppKey
        self.base_url = 'https://yun.tim.qq.com/v5/tlssmssvr/sendsms?sdkappid={}&random={}'

    def send_sms(self, code, mobile):
        send_time = int(time.time())
        sha256 = hashlib.sha256()
        random_num = random.randint(100000, 999999)
        sig_init = 'appkey={}&random={}&time={}&mobile={}'.format(
            self.AppKey, random_num, send_time, mobile)
        sha256.update(sig_init.encode('utf8'))
        sig = sha256.hexdigest()
        url = self.base_url.format(self.AppID, random_num)
        parmas = {
            "params": [
                code,
                '2',
            ],
            "sig": sig,
            "tel": {
                "mobile": mobile,
                "nationcode": "86"
            },
            "time": send_time,
            "tpl_id": 260002
        }
        data = json.dumps(parmas)
        response = requests.post(url, data=data)
        re_dict = json.loads(response.text)
        return re_dict
