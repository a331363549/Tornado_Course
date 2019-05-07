from tornado.web import url
from MxForum.MxForm.handler import RedisHandler
from MxForum.apps.community.handler import GroupHandler, GroupMemberHandler, Group_DatilHandler,PostHandler,PostDetailHandler

GROUP_URI = '/groups/'
MEMBER_URI = "/groups/([0-9]+)/members/"
GROUP_DETAIL_URI = "/groups/([0-9]+)/"
POST_URI = "/groups/([0-9]+)/posts/"
POST_DETAIL_URI = "/posts/([0-9]+)/"

urlpattern = (
    url(GROUP_URI, GroupHandler),
    url(MEMBER_URI, GroupMemberHandler),
    url(GROUP_DETAIL_URI, Group_DatilHandler),
    url(POST_URI, PostHandler),
    url(POST_DETAIL_URI, PostDetailHandler),
)
