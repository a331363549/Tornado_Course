from wtforms.fields import StringField
from wtforms_tornado import Form
# 参数需求提示
from wtforms.validators import DataRequired, Length, Email


class MessageForm(Form):
    # name = StringField("姓名")
    name = StringField("姓名", validators=[DataRequired(message="请输入姓名"), Length(min=2, max=5, message="长度为2-5之间")])
    email = StringField("邮箱", validators=[Email(message="邮箱不合法")])
    address = StringField("地址", validators=[DataRequired(message="请填写地址")])
    message = StringField("留言", validators=[DataRequired(message="请填写留言")])
