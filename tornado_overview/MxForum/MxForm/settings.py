import peewee_async

settings = {
    "static_path": "/home/ding/桌面/github/Tornado_Course/tornado_overview/MxForum/static",
    "static_url_preifx": "/static/",
    "templates": "/home/ding/桌面/github/Tornado_Course/tornado_overview/MxForum/templates",
    "secret_key": "miw5!K5mvOIXpm6a",
    "db": {
        "host": "127.0.0.1",
        "port": 3306,
        "user": "root",
        "password": "123",
        "name": "message"
    },
    "redis": {
        "host": "127.0.0.1",
        "port": 6379,
    }

}

database = peewee_async.MySQLDatabase(
    "mxforum", host="127.0.0.1", port=3306, user="root", password='123'
)
