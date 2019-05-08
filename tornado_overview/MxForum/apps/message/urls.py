from tornado.web import url
from MxForum.apps.message.handler import *

urlpattern = (
    url("/messages/", MessageHandler),

)
