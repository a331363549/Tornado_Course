import os

from tornado.web import StaticFileHandler

from ihome.apps.users import urls as user_urls

urlpattern = [
#     (r'/(.*)', StaticFileHandler,
#      dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
             ]

urlpattern += user_urls.urlpattern

# urlpattern += community_urls.urlpattern
# urlpattern += ueditor_urls.urlpattern
# urlpattern += question_urls.urlpattern
# urlpattern += messages_urls.urlpattern
# urlpattern += monitor_urls.urlpattern

# 集成ueditor 注意事项
# 前段的域名和后端的域名保持一致
