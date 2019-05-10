import os

root_path = os.path.dirname(__file__)

configs = dict(
    debug=True,
    template_path=os.path.join(root_path, 'templates'),
    static_path=os.path.join(root_path, 'static'),
)

# import peewee_async
# import os
#
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# settings = {
#     "static_path": os.path.join(BASE_DIR, 'static'),
#     # "/home/ding/桌面/github/Tornado_Course/tornado_overview/MxForum/static",
#     "static_url_preifx": "/static/",
#     "templates": os.path.join(BASE_DIR, 'templates'),
#     # "/home/ding/桌面/github/Tornado_Course/tornado_overview/MxForum/templates",
#     "secret_key": "miw5!K5mvOIXpm6a",
#     "SITE_URL": "http://192.168.79.135",
#     "jwt_expire": 7 * 24 * 3600,
#     "MEDIA_ROOT": os.path.join(BASE_DIR, 'media'),
#     "db": {
#         "host": "127.0.0.1",
#         "port": 3306,
#         "user": "root",
#         "password": "123",
#         "name": "message"
#     },
#     "redis": {
#         "host": "127.0.0.1",
#         "port": 6379,
#     },
# }
#
# database = peewee_async.MySQLDatabase(
#     "mxforum", host="127.0.0.1", port=3306, user="root", password='123'
# )