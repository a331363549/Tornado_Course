import json
import uuid
import aiofiles
import os
import random
from datetime import datetime

import jwt
from MxForum.MxForm.handler import RedisHandler
from MxForum.apps.users.forms import *
from MxForum.apps.users.models import User
from MxForum.apps.utils.AsyncYUnPian import AsyncYunPian
from MxForum.apps.utils.mxform_decorators import authenticated_async
from MxForum.apps.utils.util_func import json_serial


class MainHandler(RedisHandler):
    def get(self, *args, **kwargs):
        # self.write("hello world")
        self.render("index.html")


class ChangePasswordHandler(RedisHandler):
    @authenticated_async
    async def post(self):
        """修改密码"""
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        password_form = ChangePasswordForm.from_json(param)
        if password_form.validate():
            if not self.current_user.password.check_password(password_form.old_password.data):
                self.set_status(400)
                re_data['old_password'] = "旧密码错误"
            else:
                if password_form.new_password.data != password_form.confirm_password.data:
                    self.set_status(400)
                    re_data['comfirm_error'] = "两次输入的密码不一致"
                else:
                    self.current_user.password = password_form.new_password.data
                    await self.application.objects.update(self.current_user)
                    re_data["id"] = self.current_user.id
        else:
            self.set_status(400)
            for field in password_form.errors:
                re_data[field] = password_form.errors[field][0]
        self.finish(re_data)


class HeadImageHandler(RedisHandler):
    @authenticated_async
    async def get(self):
        self.finish = ({
            "image": "/media/" + self.current_user.head_url
        })

    @authenticated_async
    async def post(self):
        re_data = {}
        files_meta = self.request.files.get("image", None)
        if not files_meta:
            self.set_status(400)
            re_data["image"] = "请上传图片"
        else:
            # 完成验证 通过aiofiles 写文件
            new_filename = ""
            for meta in files_meta:
                filename = meta['filename']
                new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                file_path = os.path.join(self.settings['MEDIA_ROOT'], new_filename)
                async with aiofiles.open(file_path, 'wb') as f:
                    await f.write(meta['body'])
                    re_data["image"] = "/media/" + new_filename
                self.current_user.head_url = new_filename
                await self.application.objects.update(self.current_user)
        self.finish(re_data)


class ProfileHandler(RedisHandler):
    @authenticated_async
    async def get(self):
        """获取个人信息"""
        re_data = {
            "mobile": self.current_user.mobile,
            "nick_name": self.current_user.nick_name,
            "gender": self.current_user.gender,
            "address": self.current_user.address,
            "desc": self.current_user.desc
        }
        self.finish(re_data)

    @authenticated_async
    async def patch(self):
        """修改用户信息
        put 修改全部信息
        patch 修改部分信息
        """
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        profile_form = ProfileForm.from_json(param)
        if profile_form.validate():
            self.current_user.nick_name = profile_form.nick_name.data
            self.current_user.gender = profile_form.gender.data
            self.current_user.address = profile_form.address.data
            self.current_user.desc = profile_form.desc.data
            await self.application.objects.update(self.current_user)
            re_data["id"] = self.current_user.id
        else:
            self.set_status(400)
            for field in profile_form.errors:
                re_data[field] = profile_form.errors[field][0]
        self.finish(json.dumps(re_data, default=json_serial))


class LoginHandler(RedisHandler):
    async def post(self):
        re_data = {}
        param = self.request.body.decode("utf8")
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
