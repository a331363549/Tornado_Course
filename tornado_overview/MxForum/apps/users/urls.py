from tornado.web import url
from MxForum.apps.users.handler import SmsHandler,  ResgisterHandler,LoginHandler

SMS_URI = '/code/'
REGISTER_URI = "/register/"
LOGIN_URI = "/login/"

urlpattern = (
    url(SMS_URI, SmsHandler),
    url(REGISTER_URI, ResgisterHandler),
    url(LOGIN_URI, LoginHandler),
)
