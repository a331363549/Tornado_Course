from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import BIGINT, DECIMAL, DATE, TIME, DATETIME
from sqlalchemy import Column

BaseModel = declarative_base()
metadata = BaseModel.metadata  # 创建元类


class Mem(BaseModel):
    """
    内存统计模型字段
    编号　  id 大整型　主键
    使用率　percent 小数类型 允许为空
    总容量　total   小数类型 允许为空
    使用量　used    小数类型 允许为空
    剩余量　free    小数类型 允许为空
    创建日期 create_date  日期类型
    创建时间 create_time  时间类型
    创建日期时间　create_dt  日期时间类型
    """
    __tablename__ = "memory"
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


class Swap(BaseModel):
    """
    交换分区统计模型字段
    编号　  id 大整型　主键
    使用率　percent 小数类型 允许为空
    总容量　total   小数类型 允许为空
    使用量　used    小数类型 允许为空
    剩余量　free    小数类型 允许为空
    创建日期 create_date  日期类型
    创建时间 create_time  时间类型
    创建日期时间　create_dt  日期时间类型
    """
    __tablename__ = "swap"
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    total = Column(DECIMAL(8, 2))
    used = Column(DECIMAL(8, 2))
    free = Column(DECIMAL(8, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


class CPU(BaseModel):
    """
    CPU统计模型字段
    编号　  id 大整型　主键
    使用率　percent 小数类型 允许为空
    创建日期 create_date  日期类型
    创建时间 create_time  时间类型
    创建日期时间　create_dt  日期时间类型
    """
    __tablename__ = "cpu"
    id = Column(BIGINT, primary_key=True)
    percent = Column(DECIMAL(6, 2))
    create_date = Column(DATE)
    create_time = Column(TIME)
    create_dt = Column(DATETIME)


import mysql.connector
from sqlalchemy import create_engine

if __name__ == '__main__':
    mysql_configs = dict(
        db_host="127.0.0.1",
        db_name="monitor",
        db_port=3306,
        db_user="root",
        db_pwd=123,
    )
    # 连接数据库的格式：mysql+驱动名称://用户:密码@主机:端口/数据库名称
    link = "mysql+mysqlconnector://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_name}".format(**mysql_configs)
    # echo 是否输出日志
    engine = create_engine(link, encoding="utf-8", echo=True)
    # 映射
    metadata.create_all(engine)
