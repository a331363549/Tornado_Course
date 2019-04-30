import asyncio
from chapter04.models.model_async import Goods
from chapter04.models.model_async import objects


async def handler():
    # 异步插入数据
    # await objects.create(Goods, supplier_id=2, name="测试数据2", click_num=20,
    #                      goods_num=1000, price=100, brief="长沙微领地")
    goods = await objects.execute(Goods.select())
    for good in goods:
        print(good.name)

loop = asyncio.get_event_loop()
loop.run_until_complete(handler())

