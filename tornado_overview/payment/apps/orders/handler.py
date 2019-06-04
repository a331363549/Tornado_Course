import json

from datetime import datetime

from BaseFile.handler import RedisHandler
from BaseFile.settings import settings
from apps.utils.alipay import AliPay
from apps.utils.util_func import json_serial


def get_ali_object():
    app_id = "2016092900625222"
    # 支付宝向这个地址发送一个post请求,识别公网的IP,局域网连接不到
    notify_url = "http://47.98.254.88:8000/page2/"
    # 支付完成的回调地址
    return_url = "http://47.98.254.88:8000/page2/"
    # 应用私钥
    merchant_private_key_path = settings['private_key_path']
    # 应用公钥
    alipay_public_key_path = settings['ali_pub_key_path']

    alipay = AliPay(
        appid=app_id,
        app_notify_url=notify_url,
        return_url=return_url,
        app_private_key_path=merchant_private_key_path,
        alipay_public_key_path=alipay_public_key_path,
        debug=True
    )
    return alipay


class CreateOrderHandler(RedisHandler):
    """产生订单"""

    async def post(self):
        res_data = {
            "subject": "哈哈",
            "out_trande_no": datetime.now(),
            "total_amount": 0.1
        }
        self.finish(json.dumps(res_data, default=json_serial))


class payHandler(RedisHandler):
    def get(self):
        # self.write("hello world")
        self.render("index.html")
        # self.redirect("http://127.0.0.1")

    def post(self):
        pass


class GenPayLinkHandler(RedisHandler):
    async def post(self):
        money = float(self.get_argument("money"))
        alipay = AliPay(
            appid=self.settings['ALI_APPID'],
            app_notify_url='{}/alipay/return/'.format(settings["SITE_URL"]),
            app_private_key_path=settings["private_key_path"],
            alipay_public_key_path=settings["ali_pub_key_path"],
            debug=True,
            return_url='{}/alipay/return/'.format(settings["SITE_URL"])
        )
        # 生成支付宝的url
        query_params = alipay.direct_pay(
            subject="哈哈哈",
            out_trade_no="x2" + str(datetime.now()),
            total_amount=money
        )
        pay_url = "https://openapi.alipaydev.com/gateway.do?{0}".format(query_params)  # 支付宝网关地址（沙箱应用）
        print(pay_url)
        return self.finish(pay_url)
        # redirect 跳转到制定的链接
        # return self.redirect(pay_url)


class AlipayHandler(RedisHandler):
    """处理return_url"""

    def get(self):
        res_data = {}
        processed_dict = {}
        req_data = self.request.arguments
        # req_data = format_arguments(req_data)
        for key, value in req_data.items():
            processed_dict[key] = value[0]

        sign = processed_dict.pop('sign', None)
        alipay = AliPay(
            appid=settings["ALI_APPID"],
            app_notify_url="{}/alipay/return/".format(settings["SITE_URL"]),
            app_private_key_path=settings["private_key_path"],
            alipay_public_key_path=settings["ali_pub_key_path"],
            debug=True,
            return_url="{}/alipay/return/".format(settings["SITE_URL"])
        )
        verify_re = alipay.verify(processed_dict, sign)
        if verify_re is True:
            res_data["content"] = "success"
        else:
            res_data["content"] = "failed"

        self.finish(res_data)

    async def post(self):
        """处理notify_url"""
        re_data = {}
        processed_dict = {}
        req_data = self.request.arguments
        # req_data = format_arguments(req_data)
        for key, value in req_data.items():
            processed_dict[key] = value[0]

        sign = processed_dict.pop('sign', None)
        alipay = AliPay(
            appid=settings["ALI_APPID"],
            app_notify_url="{}/alipay/return/".format(settings["SITE_URL"]),
            app_private_key_path=settings["private_key_path"],
            alipay_public_key_path=settings["ali_pub_key_path"],
            debug=True,
            return_url="{}/alipay/return/".format(settings["SITE_URL"])
        )
        verify_re = alipay.verify(processed_dict, sign)

        if verify_re is True:
            print("excute sql")
            re_data['content'] = processed_dict
        else:
            print("failed")
            re_data['content'] = "failed"
        self.finish(re_data)

# class AlipayHandler(RedisHandler):
#     """处理支付宝return_url"""
#     def get(self):
#         # 检测是否支付成功
#         # 去请求体中获取所有返回的数据：状态/订单号
#         alipay = get_ali_object()
#         # name&age=123....
#         # body_str = self.request.body.decode('utf-8')
#         # post_data = parse_qs(body_str)
#
#         post_dict = {}
#         # for k, v in post_data.items():
#         #     post_dict[k] = v[0]
#         post_dict = self.request.arguments
#         # post_dict有10key： 9 ，1
#         sign = post_dict.pop('sign', None)[0]
#         status = alipay.verify(post_dict, sign)
#         print('------------------开始------------------')
#         print('GET验证', status)
#         print(post_dict)
#         out_trade_no = post_dict['out_trade_no']
#
#         # 修改订单状态
#         # models.Order.objects.filter(trade_no=out_trade_no).update(status=2)
#         print('------------------结束------------------')
#         # 修改订单状态：获取订单号
#         return self.write('POST返回')
#
#     def post(self):
#         alipay = get_ali_object()
#         print(self.request.arguments)
#         params = self.request.arguments
#         sign = params.pop('sign', None)[0]
#         status = alipay.verify(params, sign)
#         print('==================开始==================')
#         print('POST验证', status)
#         print('==================结束==================')
#         return self.write('支付成功')
