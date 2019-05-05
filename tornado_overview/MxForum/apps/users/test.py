import requests
from MxForum.apps.users.urls import SMS_URI, REGISTER_URI
import json

web_url = "http://127.0.0.1:8888"


def test_sms():
    url = web_url + SMS_URI
    data = {
        "mobile": "18565607772"
    }
    res = requests.post(url, json=data)
    print(json.loads(res.text))


def test_register():
    url = web_url + REGISTER_URI
    data = {
        "mobile": "18565607772",
        "code": "398105",
        "password": "111111",
    }
    res = requests.post(url, json=data)
    print(json.loads(res.text))


if __name__ == '__main__':
    test_sms()
    # test_register()
