from peewee import *

from MxForum.apps.users.models import User

# from apps.community.models import CommunityGroup, CommunityGroupMember, Post, PostComment, CommentLike
# from apps.question.models import *

from MxForum.MxForm.settings import database


# 设置是否同步
database.set_allow_sync(True)

def init():
    # 生成表
    database.create_tables([User])
    # database.create_tables([CommunityGroup,CommunityGroupMember])
    # database.create_tables([Post, PostComment, CommentLike])
    # database.create_tables([Question, Answer])


if __name__ == "__main__":
    init()
