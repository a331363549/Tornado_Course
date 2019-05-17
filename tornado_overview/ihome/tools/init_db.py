from ihome.home.settings import database

from ihome.apps.users.models import *


def init():
    # 生成表
    database.create_tables([User])
    # database.create_tables([Order])
    # database.create_tables([Question, Answer])
    # database.create_tables([Message])
    # database.create_tables([Mem, Swap, Cpu])


if __name__ == "__main__":
    init()
