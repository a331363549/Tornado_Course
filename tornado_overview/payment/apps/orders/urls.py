from tornado.web import url
from apps.orders.handler import *

urlpattern = (
    url('/pay_ali/', payHandler),
    url('/order/', CreateOrderHandler),
    url('/page1/', GenPayLinkHandler),
    url('/alipay/return/', AlipayHandler)
)
