from chatper04.models.model import Suppliner, Goods
from chatper04.data import supplier_list, goods_list


def save_model():
    for data in supplier_list:
        supplier = Suppliner()
        supplier.name = data["name"]
        supplier.address = data["address"]
        supplier.phone = data["phone"]
        supplier.save()

    for data in goods_list:
        good = Goods(**data)
        good.save()


# 查询数据
def query_model():
    """
    获取某条数据
    # 方法1：
    good1 = Goods.get(Goods.id == 1)
    # 方法2：
    good2 = Goods.get_by_id(1)
    # 方法3：
    good3 = Goods[1]
    print(good1.name+'\n' + good2.name+'\n' + good3.name)
    """

    """
    获取所有数据
    1.返回指定的数据 下语句返回的是物品的名称与价格
    goods = Goods.select(Goods.name, Goods.price_num)
    
    2.select * from goods where price > 100 的实现
    goods = Goods.select().where(Goods.price>100）
    
    3.select * from goods where price > 100 and click_num >200 的实现
    goods = Goods.select().where((Goods.price>100) & （Goods.click_num>200))
    
    4.select * from goods where name like "%飞天"
    goods = Goods.select().where((Goods.name.contains("飞天"))
    
    5. 排序
    升序
    goods = Goods.select().order_by(Goods.price.asc())
    goods = Goods.select().order_by(Goods.price) 
    降序
    goods = Goods.select().order_by(Goods.price.desc()) 
    goods = Goods.select().order_by(-Goods.price)
    
    # 分页
    goods = Goods.select().order_by(Goods.price).paginate(2,2) 
    
    """
    # select * from goods
    goods = Goods.select()
    for good in goods:
        print(good.name)


# 更新数据
def update_model():
    # 增加click_num数量
    good = Goods.get_by_id(1)
    good.click_num += 1
    good.save()

    # update click_num=100 where id = 1  需要调用execute()才能执行
    Goods.update(click_num=100).where(Goods.id == 1).execute()

    # 删除当前记录
    # good.delete_instance()

    # delete freom goods from where price > 150
    Goods.delete().where(Goods.price_num > 150).execute()


if __name__ == '__main__':
    # save_model()
    query_model()
