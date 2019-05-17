import requests

apikey = "c79fce9f19673ffb7f2b365a684ddaf0"


class YunPiansms:
    def __init__(self, api_key):
        self.api_key = api_key

    # 发送单条短信
    def send_single_sms(self, code, mobile):
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【测试使用】您的验证码是{},如非本人操作,请忽略本短信".format(code)
        res = requests.post(url, data={
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        })
        return res


if __name__ == '__main__':
    yun = YunPiansms("c79fce9f19673ffb7f2b365a684ddaf0")
    res = yun.send_single_sms("8888", "18565607772")
    print(res.text)
