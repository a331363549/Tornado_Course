from tornado.web import url
from MxForum.apps.users.handler import *

SMS_URI = '/code/'
REGISTER_URI = "/register/"
LOGIN_URI = "/login/"
INFO_URI = "/info/"
HEADIMAGE_URI = "/headimages/"
PASSWORD_URI = "/password/"

urlpattern = (
    url('/', MainHandler),
    url(SMS_URI, SmsHandler),
    url(REGISTER_URI, ResgisterHandler),
    url(LOGIN_URI, LoginHandler),
    url(INFO_URI, ProfileHandler),
    url(HEADIMAGE_URI, HeadImageHandler),
    url(PASSWORD_URI, ChangePasswordHandler)
)
