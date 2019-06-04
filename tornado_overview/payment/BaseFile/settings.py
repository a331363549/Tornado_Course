import peewee_async
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
settings = {
    "static_path": os.path.join(BASE_DIR, 'static'),
    # "/home/ding/桌面/github/Tornado_Course/tornado_overview/MxForum/static",
    "static_url_preifx": "/static/",
    "template_path": os.path.join(BASE_DIR, 'templates'),
    # "/home/ding/桌面/github/Tornado_Course/tornado_overview/MxForum/templates",
    "secret_key": "miw5!K5mvOIXpm6a",
    "SITE_URL": "http://47.98.554.88",
    "jwt_expire": 7 * 24 * 3600,
    "MEDIA_ROOT": os.path.join(BASE_DIR, 'media'),
    "db": {
        "host": "47.98.554.88",
        "port": 3306,
        "user": "root",
        "password": "123",
        "name": "message"
    },
    "redis": {
        "host": "47.98.554.88",
        "port": 6379,
    },
    "ALI_APPID": "2016092900625222",
    "private_key_path": os.path.join(BASE_DIR, "keys", 'app_private_2048.txt'),
    "ali_pub_key_path": os.path.join(BASE_DIR, 'keys', 'alipay_public_2048.txt'),

}

database = peewee_async.MySQLDatabase(
    "mydb", host="47.98.554.88", port=3306, user="root", password='123'
)
