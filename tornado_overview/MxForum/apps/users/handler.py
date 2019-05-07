import json
import random
from datetime import datetime

import jwt
from MxForum.MxForm.handler import RedisHandler
from MxForum.apps.users.forms import SmsCodeForm, RegisterForm, LoginForm
from MxForum.apps.users.models import User
from MxForum.apps.utils.AsyncYUnPian import AsyncYunPian


class MainHandler(RedisHandler):
    def get(self, *args, **kwargs):
        self.write("hello world")


class LoginHandler(RedisHandler):
    async def post(self):
        re_data = {}
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        login_form = LoginForm.from_json(param)
        if login_form.validate():
            mobile = login_form.mobile.data
            password = login_form.password.data
            try:
                user = await self.application.objects.get(User, mobile=mobile)
                if not user.password.check_password(password):
                    self.set_status(400)
                    re_data['non_fields'] = "用户名或密码错误"
                else:
                    # 登录成功
                    # 生成json web token
                    payload = {
                        "id": user.id,
                        "nick_name": user.nick_name,
                        "exp": datetime.utcnow()
                    }
                    token = jwt.encode(payload, self.settings["secret_key"], algorithm="HS256")
                    re_data['id'] = user.id
                    if user.nick_name is not None:
                        re_data['nick_name'] = user.nick_name
                    else:
                        re_data['nick_name'] = user.mobile
                    re_data['token'] = token.decode('utf8')
            except User.DoesNotExist as e:
                self.set_status(400)
                re_data['mobile'] = "用户不存在"

            self.finish(re_data)


class ResgisterHandler(RedisHandler):
    async def post(self):
        re_data = {}
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data
            # 验证码是否正确
            redis_key = "{}_{}".format(mobile, code)
            if not self.redis_conn.get(redis_key):
                self.set_status(400)
                re_data['code'] = "验证码错误或失效"
            else:
                # 用户是否存在
                try:
                    existed_users = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    re_data['mobile'] = "用户已存在"
                except User.DoesNotExist as e:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    re_data['id'] = user.id
                # except User.DoesNotExist as e:
                #     user = await self.application.objects.create(User, mobile=mobile, password=password)
                #     re_data['id'] = user.id
        else:
            self.set_status(400)
            for field in register_form.errors:
                re_data[field] = register_form.errors[field][0]
        self.finish(re_data)


class SmsHandler(RedisHandler):
    def generateCode(self):
        sms_code = "%04d" % random.randint(0, 10000)
        return sms_code

    async def post(self):
        re_data = {}
        param = self.request.body.decode("utf-8")
        param = json.loads(param)
        sms_form = SmsCodeForm.from_json(param)
        if sms_form.validate():
            mobile = sms_form.mobile.data
            code = self.generateCode()
            yun_pian = AsyncYunPian("d6c4ddbf50ab36611d2f52041a0b949e")
            re_json = await yun_pian.send_sigle_sms(code, mobile)
            if re_json["code"] != 0:
                self.set_status(400)
                re_data["mobile"] = re_json['msg']
            else:
                # 将验证码写入redies
                self.redis_conn.set("{}_{}".format(mobile, code), 1, 10 * 60)
        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]
        self.finish(re_data)