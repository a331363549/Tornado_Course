from tornado.web import url
from MxForum.apps.community.handler import *

GROUP_URI = '/groups/'
MEMBER_URI = "/groups/([0-9]+)/members/"
GROUP_DETAIL_URI = "/groups/([0-9]+)/"
POST_URI = "/groups/([0-9]+)/posts/"
POST_DETAIL_URI = "/posts/([0-9]+)/"
COMMENT_URI = "/posts/([0-9]+)/comments/"
COMMENT_REPLY_URI = "/comments/([0-9]+)/replys/"
LIKES_URI = "/comments/([0-9]+)/likes/"

urlpattern = (
    url(GROUP_URI, GroupHandler),
    url(MEMBER_URI, GroupMemberHandler),
    url(GROUP_DETAIL_URI, Group_DatilHandler),
    url(POST_URI, PostHandler),
    url(POST_DETAIL_URI, PostDetailHandler),
    url(COMMENT_URI, PostCommentHandler),
    url(COMMENT_REPLY_URI, CommentReplayHandler),
    url(LIKES_URI, LikeHandler),

)
