from peewee import *
from datetime import datetime

db = MySQLDatabase("message", host="127.0.0.1", port=3306, user="root", password='123')


class BaseModel(Model):
    add_time = DateTimeField(default=datetime.now, verbose_name='添加时间')

    class Meta:
        database = db


class Suppliner(BaseModel):
    name = CharField(max_length=100, verbose_name="名称", index=True)
    address = CharField(max_length=100, verbose_name="联系地址", index=True)
    phone = CharField(max_length=11, verbose_name='联系方式')

    class Meta:
        table_name = "supplier"


class Goods(BaseModel):
    supplier = ForeignKeyField(Suppliner, verbose_name='商家', backref='goods')
    name = CharField(max_length=100, verbose_name="商品名称", index=True)
    click_num = IntegerField(default=0, verbose_name='点击数')
    goods_num = IntegerField(default=0, verbose_name='库存')
    price_num = FloatField(default=0, verbose_name='价格')
    breif = TextField(default="", verbose_name="商品简介")

    class Meta:
        table_name = "goods"


def init_table():
    db.create_tables([Goods,Suppliner])


if __name__ == '__main__':
    init_table()
