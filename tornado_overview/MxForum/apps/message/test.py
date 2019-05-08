import json
from datetime import datetime
import requests
import jwt

current_time = datetime.utcnow()

from MxForum.MxForm.settings import settings

web_site_url = "http://127.0.0.1:8888"
data = jwt.encode({
    "name": "bobby",
    "id": 1,
    "exp": current_time
}, settings["secret_key"]).decode("utf8")

headers = {
    "tsessionid": data
}



def add_post(group_id):
    """发帖"""
    data = {
        "title": "我是标题",
        "content": "我是评论",
    }
    res = requests.post("{}/groups/{}/posts/".format(web_site_url, group_id), headers=headers, json=data)
    print(res.status_code)
    print(json.loads(res.text))




def get_comment(post_id):
    """获取帖子评论"""
    res = requests.get("{}/posts/{}/comments/".format(web_site_url, post_id), headers=headers)
    print(res.status_code)
    print(json.loads(res.text))


if __name__ == '__main__':
    # new_group()
    # apply_group(1, "test")
    # add_post(1)
    # get_post(100)
    # add_comment(1)
    # get_comment(1)
    add_replys(1)
