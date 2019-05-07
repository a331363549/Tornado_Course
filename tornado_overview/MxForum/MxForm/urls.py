from MxForum.apps.users import urls as user_urls
from MxForum.apps.community import urls as community_urls
from MxForum.apps.question import urls as question_urls
from tornado.web import url, StaticFileHandler
from MxForum.apps.ueditor import urls as ueditor_urls
from MxForum.MxForm.settings import settings

urlpattern = [
    (url("/media/(.*)", StaticFileHandler, {'path': settings["MEDIA_ROOT"]}))
]

urlpattern += user_urls.urlpattern
urlpattern += community_urls.urlpattern
urlpattern += ueditor_urls.urlpattern

# 集成ueditor 注意事项
# 前段的域名和后端的域名保持一致
