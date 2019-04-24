import re

from utils.response_code import RET
from .BaseHandler import BaseHandler
from utils.captcha.captcha import captcha

import random
import logging
import constants
from libs.yuntongxun.CCP import ccp


class ImageCodeHandler(BaseHandler):
    def get(self):
        code_id = self.get_argument("codeid")
        pre_code_id = self.get_argument("pcodeid")
        # 生成图片验证码
        name, text, image = captcha.generate_captcha()
        try:
            if pre_code_id:
                self.redis.delete("image_code_%s" % pre_code_id)
            self.redis.setex("image_code_%s" % pre_code_id, constants.PIC_CODE_EXPIRES_SECONDS, text)
        except Exception as e:
            logging.error(e)
            self.write("")
        else:
            self.set_header("Content-Type", "image/jpg")
            self.write(image)


class SMSCodeHandler(BaseHandler):
    def post(self):
        global real_image_code_text
        mobile = self.json_args.get("mobile")
        image_code_id = self.json_args.get("image_code_id")
        image_code_text = self.json_args.get("image_code_text")
        if not all((mobile, image_code_id, image_code_text)):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="参数不完整"))
        if not re.match(r'1\d{10}$', mobile):
            return self.write(dict(errcode=RET.PARAMERR, errmsg="手机号格式错误"))

        # 判断图片验证码
        try:
            real_image_code_text = self.redis.get("image_code_%s" % image_code_id).decode()
        except Exception as e:
            logging.error(e)
            self.write(dict(errcode=RET.DBERR, errmsg="查询验证码错误"))

        if not real_image_code_text:
            return self.write(dict(errcode=RET.NODATA, errmsg="验证码已过期"))

        if real_image_code_text.lower() != image_code_text.lower():
            return self.write(dict(errcode=RET.DATAERR, errmsg="验证码错误！"))

        # 删除图片验证码
        try:
            self.redis.delete("image_code_%s" % image_code_id)
        except Exception as e:
            logging.error(e)

        # 手机号是否存在
        sql = "select count(*) counts from ih_user_profile where up_mobile=%s "
        try:
            ret = self.db.get(sql, mobile)
        except Exception as e:
            logging.error(e)
        else:
            if 0 != ret["counts"]:
                return self.write(dict(errcode=RET.DATAEXIST, errmsg="手机号已注册"))

        # 验证成功
        sms_code = "%06d" % random.randint(0, 1000000)
        try:
            self.redis.setex("sms_code_%s" % mobile, constants.SMS_CODE_EXPIRES_SECONDS, sms_code)
        except Exception as e:
            logging.error(e)
            self.write(dict(errcode=RET.DBERR, errmsg="生成短信验证码错误"))

        # 发送验证码
        try:
            result = ccp.sendTemplateSMS(mobile, [sms_code, constants.SMS_CODE_EXPIRES_SECONDS/60], 1)
        except Exception as e:
            logging.error(e)
            return self.write(dict(errcode=RET.THIRDERR, errmsg="发送失败"))
        if result:
            self.write(dict(errcode=RET.OK, errmsg="OK"))
        else:
            return self.write(dict(errcode=RET.THIRDERR, errmsg="发送失败"))
