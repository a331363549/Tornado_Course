import os

# Application cofigure
settings = dict(static_path=os.path.join(os.path.dirname(__file__), "static"),
                template_path=os.path.join(os.path.dirname(__file__), "template"),
                cookie_secret="K4KsZdGJRK6ejgaiBb4THetTtljKf0G6sUzNz4gkksc=",
                xsrf_cookies=True,
                debug=True)

# MySQL
mysql_option = dict(
    host="127.0.0.1",
    database="ihome",
    user="root",
    password="123"
)

# redis
redis_option = dict(
    host="127.0.0.1",
    port=6379,
)

# log_file
log_file = os.path.join(os.path.dirname(__file__),"logs/log")
log_lever = "debug"

# 密码加密密钥
passwd_hash_key = "nlgCjaTXQX2jpupQFQLoQo5N4OkEmkeHsHD9+BBx2WQ="