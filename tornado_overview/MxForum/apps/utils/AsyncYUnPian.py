from tornado import httpclient
from tornado.httpclient import HTTPRequest
from urllib.parse import urlencode
import tornado
from functools import partial
import json


class AsyncYunPian:
    def __init__(self, api_key):
        self.api_key = api_key

    async def send_sigle_sms(self, code, mobile):
        http_client = httpclient.AsyncHTTPClient()
        url = "https://sms.yunpian.com/v2/sms/single_send.json"
        text = "【慕学生鲜】您的验证码是{}。如非本人操作，请忽略本短信".format(code)
        post_request = HTTPRequest(url=url, method="POST", body=urlencode({
            "apikey": self.api_key,
            "mobile": mobile,
            "text": text
        }))
        res = await http_client.fetch(post_request)
        return json.loads(res.body.decode("utf8"))


if __name__ == '__main__':
    io_loop = tornado.ioloop.IOLoop.current()
    yunpian = AsyncYunPian("d6c4ddbf50ab36611d2f52041a0b949e")
    # 将带参数的方法封装成一个新的方法
    new_func = partial(yunpian.send_sigle_sms, "8888", "18565607772")
    io_loop.run_sync(new_func)
