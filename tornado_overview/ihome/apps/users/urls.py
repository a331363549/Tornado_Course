from tornado.web import url
from ihome.apps.users.handler import *

SMS_URI = '/code/'

urlpattern = (
    url(r"/", MainHandler),
    url(r'/login/', LoginHandler),
    url(r"/register/", RegisterHandler),
    url(r'/code/', SmsHandler),
    # url(r"/info/", ProfileHandler),
    # url(r"/headimages/", HeadImageHandler),
    # url(r"/password/", ChangePasswordHandler)
)
