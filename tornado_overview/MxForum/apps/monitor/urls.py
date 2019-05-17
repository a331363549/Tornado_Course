from tornado.web import url
from MxForum.apps.monitor.handler import *
from sockjs.tornado import SockJSRouter

urlpattern = (
                 url("/", SystemInfoHandler),
                 url("/log/", LogHandler),
             )
