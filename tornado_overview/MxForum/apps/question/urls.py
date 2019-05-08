from tornado.web import url
from MxForum.apps.question.handler import *

urlpattern = (
    url("/questions/", QuestionHandler),
    url("/questions/([0-9]+)/", QuestionDetailHandler),
    url("/questions/([0-9]+)/answers/", AnswerHandler),
    url("/answers/([0-9]+)/replys/", AnswerReplyHandler),
)
