from tornado.web import url
from MxForum.apps.users.handler import *


urlpattern = (
    # url('/', MainHandler),
    url(r'/code/', SmsHandler),
    url(r"/register/", ResgisterHandler),
    url(r"/login/", LoginHandler),
    url(r"/info/", ProfileHandler),
    url(r"/headimages/", HeadImageHandler),
    url(r"/password/", ChangePasswordHandler)
)
