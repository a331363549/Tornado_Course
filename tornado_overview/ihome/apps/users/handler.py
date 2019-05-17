import json
import random
import uuid

import jwt

from MxForum.MxForm.handler import RedisHandler
# 用戶是否已登录
from ihome.apps.users.models import *
from ihome.apps.users.forms import *
from MxForum.apps.utils.AsyncYUnPian import AsyncYunPian
import aiofiles
import os
from playhouse.shortcuts import model_to_dict
from MxForum.apps.utils.util_func import json_serial


class MainHandler(RedisHandler):
    def get(self, *args, **kwargs):
        pass
        # self.render("index.html")
        # return self.render_string("login.html", order=order, cal_total=self.cal_total)


class ProfileHandler(RedisHandler):
    """个人信息修改"""
    async def post(self, *args, **kwargs):
        re_date = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        login_form = ProfileForm.from_json(param)



class LoginHandler(RedisHandler):
    """登录"""
    async def post(self, *args, **kwargs):
        re_date = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        login_form = LoginForm.from_json(param)
        if login_form.validate():
            mobile = login_form.mobile.data
            password = login_form.password.data
            try:
                user = await self.application.objects.get(User, mobile=mobile)
                if not user.password.check_password(password=password):
                    self.set_status(400)
                    re_date["error"] = "用户名或密码错误"
                else:
                    payload = {
                        "id": user.id,
                        "nick_name": user.nick_name,
                        "exp": datetime.utcnow()
                    }
                    token = jwt.encode(payload, self.settings["secret_key"], algorithm="HS256")
                    re_date['id'] = user.id
                    if user.nick_name is not None:
                        re_date['nick_name'] = user.nick_name
                    else:
                        re_date['nick_name'] = user.mobile
                    re_date['token'] = token.decode('utf8')
            except User.DoesNotExist:
                self.set_status(400)
                re_date["mobile"] = "用户不存在"
        else:
            self.set_status(400)
            for field in login_form.errors:
                re_date[field] = login_form.errors[field][0]
        self.finish(re_date)


class RegisterHandler(RedisHandler):
    async def post(self, *args, **kwargs):
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        register_form = RegisterForm.from_json(param)
        if register_form.validate():
            mobile = register_form.mobile.data
            code = register_form.code.data
            password = register_form.password.data
            # 验证验证码
            redis_key = "{}_{}".format(mobile, code)
            if not self.redis_conn.get(redis_key):
                self.set_status(400)
                re_data['code'] = "验证码错误或失效"
            else:
                try:
                    exist_user = await self.application.objects.get(User, mobile=mobile)
                    self.set_status(400)
                    re_data["mobile"] = "用户已存在"
                except User.DoesNotExist:
                    user = await self.application.objects.create(User, mobile=mobile, password=password)
                    re_data['id'] = user.id
        else:
            self.set_status(400)
            for field in register_form.errors:
                re_data[field] = register_form.errors[field][0]
        self.finish(re_data)


class SmsHandler(RedisHandler):
    def generateCode(self):
        sms_code = "%04d" % random.randint(0, 10000)
        return sms_code

    async def post(self, *args, **kwargs):
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        sms_form = SmsCodeForm.from_json(param)
        if sms_form.validate():
            mobile = sms_form.mobile.data
            code = self.generateCode()
            msm = AsyncYunPian("d6c4ddbf50ab36611d2f52041a0b949e")
            re_json = await msm.send_sigle_sms(code, mobile)
            if re_json["code"] != 0:
                self.set_status(400)
                re_data['mobile'] = re_json['msg']
            else:
                re_data["code"] = code
                self.redis_conn.set("{}_{}".format(mobile, code), 1, 10 * 60)
        else:
            self.set_status(400)
            for field in sms_form.errors:
                re_data[field] = sms_form.errors[field][0]
        self.finish(re_data)
