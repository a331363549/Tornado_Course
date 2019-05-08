from MxForum.MxForm.settings import database
from MxForum.apps.users.models import User

from MxForum.apps.community.models import *
from MxForum.apps.question.models import *
from MxForum.apps.message.models import *


def init():
    # 生成表
    database.create_tables([User])
    database.create_tables([CommunityGroup, CommunityGroupMember, Post, PostComment, CommentLike])
    database.create_tables([Question, Answer])
    database.create_tables([Message])


if __name__ == "__main__":
    init()
