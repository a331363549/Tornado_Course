from sockjs.tornado import SockJSRouter

from MxForum.apps.users import urls as user_urls
from MxForum.apps.community import urls as community_urls
from MxForum.apps.question import urls as question_urls
from MxForum.apps.message import urls as messages_urls
from tornado.web import url, StaticFileHandler
from MxForum.apps.ueditor import urls as ueditor_urls
from MxForum.apps.monitor import urls as monitor_urls
from MxForum.MxForm.settings import settings
from MxForum.apps.monitor.handler import RealTimeHandler

urlpattern = [
                 (url("/media/(.*)", StaticFileHandler, {'path': settings["MEDIA_ROOT"]}))
             ] + SockJSRouter(RealTimeHandler, "/real/time").urls

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern
urlpattern += ueditor_urls.urlpattern
urlpattern += question_urls.urlpattern
urlpattern += messages_urls.urlpattern
urlpattern += monitor_urls.urlpattern

# 集成ueditor 注意事项
# 前段的域名和后端的域名保持一致
