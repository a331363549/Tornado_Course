from datetime import datetime

from ihome.home.models import BaseModel
from peewee import *
from bcrypt import hashpw, gensalt


class PasswordHash(bytes):
    def check_password(self, password):
        password = password.encode("utf-8")
        return hashpw(password, self) == self


class PasswordField(BlobField):
    def __init__(self, iterations=12, *args, **kwargs):
        if None in (hashpw, gensalt):
            raise ValueError('Missing library required for PasswordField:bcrypt')
        self.bcrypt_iuterations = iterations
        self.raw_password = None
        super(PasswordField, self).__init__(*args, **kwargs)

    def db_value(self, value):
        if isinstance(value, PasswordHash):
            return bytes(value)
        if isinstance(value, str):
            value = value.encode('utf-8')
        salt = gensalt(self.bcrypt_iuterations)
        return value if value is None else hashpw(value, salt)

    def python_value(self, value):
        if isinstance(value, str):
            value = value.encode('utf-8')
        return PasswordHash(value)


GENDERS = (
    ("famale", "女"),
    ("male", "男")

)


class User(BaseModel):
    mobile = CharField(max_length=11, verbose_name="手机号码", index=True, unique=True)
    password = PasswordField(verbose_name="密码")  # 1.密文  2.不可反解
    nick_name = CharField(max_length=20, null=True, verbose_name="昵称")
    real_name = CharField(max_length=20, null=True, verbose_name="真实姓名")
    user_id_card = CharField(max_length=18, null=True, verbose_name="身份证号码")
    head_url = CharField(max_length=200, default="", null=True, verbose_name="用户头像")
    lupdate_time = DateTimeField(default=datetime.now(), verbose_name="最近更新时间")
    # gender = CharField(max_length=200, choices=GENDERS, null=True, verbose_name="性别")
