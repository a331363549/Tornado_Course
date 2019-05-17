from MxForum.MxForm.models import BaseModel
from peewee import *


class Mem(BaseModel):
    """内存统计"""
    percent = FloatField(default=0, verbose_name="使用率")
    total = FloatField(default=0, verbose_name="总内存")
    used = FloatField(default=0, verbose_name="已使用")
    free = FloatField(default=0, verbose_name="空闲")
    create_date = DateTimeField(verbose_name="创建日期")
    create_time = DateTimeField(verbose_name="创建时间")


class Swap(BaseModel):
    """交换分区统计"""
    percent = FloatField(default=0, verbose_name="使用率")
    total = FloatField(default=0, verbose_name="总内存")
    used = FloatField(default=0, verbose_name="已使用")
    free = FloatField(default=0, verbose_name="空闲")
    create_date = DateTimeField(verbose_name="创建日期")
    create_time = DateTimeField(verbose_name="创建时间")


class Cpu(BaseModel):
    """cpu统计"""
    percent = FloatField(default=0, verbose_name="使用率")
    create_date = DateTimeField(verbose_name="创建日期")
    create_time = DateTimeField(verbose_name="创建时间")

