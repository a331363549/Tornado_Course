from tornado.web import url
from MxForum.MxForm.handler import RedisHandler
from MxForum.apps.community.handler import GroupHandler

GROUP_URI = '/groups/'


urlpattern = (
    url(GROUP_URI, GroupHandler),
    # url(SMS_URI, SmsHandler),
    # url(REGISTER_URI, ResgisterHandler),
    # url(LOGIN_URI, LoginHandler),
)
