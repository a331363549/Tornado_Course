import aiomysql
import asyncio
from aiomysql import create_pool
from tornado import gen, httpclient, ioloop


async def go():
    async with create_pool(host='127.0.0.1', port=3306,
                           user='root', password='123',
                           db='message', charset="utf8") as pool:
        async with pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute("SELECT * from message")
                value = await cur.fetchone()
                print(value)


if __name__ == '__main__':
    io_loop = ioloop.IOLoop.current()
    io_loop.run_sync(go)
