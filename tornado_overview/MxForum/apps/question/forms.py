from wtforms_tornado import Form
from wtforms import StringField, TextAreaField, IntegerField
from wtforms.validators import DataRequired, Regexp, AnyOf, Length

MOBILE_REGEX = "^1[358]\d{9}$|^1[48]7\d{8}$|^176\d{8}$|^1[48]5\d{8}"


class QuestionForm(Form):
    category = StringField("类别", validators=[AnyOf(values=["技术问答", "技术分享", "活动建议"])])
    title = StringField("标题", validators=[DataRequired(message="请输入标题")])
    content = TextAreaField("内容", validators=[DataRequired(message="请输入内容")])


class AnswerForm(Form):
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=3, message="内容不能少于3个字符")])


class AnswerReplyForm(Form):
    replyed_user = IntegerField("回复用户", validators=[DataRequired("请输入回复用户")])
    content = StringField("内容", validators=[DataRequired("请输入评论内容"),
                                            Length(min=3, message="内容不能少于3个字符")])
