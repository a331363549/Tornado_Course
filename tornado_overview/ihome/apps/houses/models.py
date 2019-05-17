from datetime import datetime

from ihome.home.models import BaseModel
from ihome.apps.users.models import User
from peewee import *


class HousesInfo(BaseModel):
    user = ForeignKeyField(User, verbose_name="用户")
    title = CharField(max_length=20, null=False, verbose_name="房屋名称")
    price = IntegerField(null=False, verbose_name="房屋价格")
    # area_id = ForeignKeyField()
    address = CharField(max_length=200, default="", verbose_name="房屋地址")
    room_count = IntegerField(verbose_name="房间数量")
    areage = IntegerField(verbose_name="房屋面积")
    capacity = IntegerField(verbose_name="可容纳人数")
    beds = CharField(max_length=200, verbose_name="床配置")
    deposit = IntegerField(verbose_name="押金")
    min_days = IntegerField(verbose_name="最小入住天数", default=1)
    max_days = IntegerField(verbose_name="最大入住天数", default=-1)
    order_count = IntegerField(verbose_name="下单数量", default=0)
    verify_status = SmallIntegerField()
