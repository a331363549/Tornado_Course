from datetime import datetime

from MxForum.MxForm.models import BaseModel
from peewee import *

from MxForum.apps.users.models import User



MESSAGE_TYPE = (
    (1, "评论"),
    (2, "帖子回复"),
    (3, "点赞"),
    (4, "回答"),
    (5, "回答回复"),
)


class Message(BaseModel):
    sender = ForeignKeyField(User, verbose_name="发送者")
    receiver = ForeignKeyField(User, verbose_name="接收者")
    message_type = CharField(choices=MESSAGE_TYPE, max_length=10, null=True, verbose_name="加入状态")
    message = CharField(max_length=500, null=True, verbose_name="消息内容")
    parent_content = CharField(max_length=500, null=True, verbose_name="内容")


