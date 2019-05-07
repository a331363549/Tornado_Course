import json
import uuid

from MxForum.MxForm.handler import RedisHandler
# 用戶是否已登录
from MxForum.apps.question.models import *
from MxForum.apps.question.forms import *
from MxForum.apps.utils.mxform_decorators import authenticated_async

import aiofiles
import os
from playhouse.shortcuts import model_to_dict
from MxForum.apps.utils.util_func import json_serial


class AnswerHandler(RedisHandler):
    @authenticated_async
    async def get(self, question_id):
        """获取问题的所有回答"""
        re_data = []
        try:
            question = await self.application.objects.get(Question, id=int(question_id))
            answer = await self.application.objects.execute(
                Answer.extend().where(Answer.question == question, Answer.parent_answer.is_null(True)).order_by(
                    Answer.add_time.desc())
            )
            for item in answer:
                item_dict = {
                    "user": model_to_dict(item.user),
                    "content": item.content,
                    "reply_nums": item.reply_nums,
                    "add_time": item.add_time.strftime("%Y-%m-%d"),
                    "id": item.id
                }
                re_data.append(item_dict)
        except Question.DoesNotExist as e:
            self.set_status(404)
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, question_id):
        """新增回答"""
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = AnswerForm.from_json(param)
        if form.validate():
            try:
                question = await self.application.objects.get(Question, id=int(question_id))
                answer = await self.application.objects.create(Answer, user=self.current_user,
                                                               question=question,
                                                               content=form.content.data)
                question.answer_nums += 1
                await self.application.objects.update(question)
                re_data["id"] = answer.id
                re_data["user"] = {
                    "nick_name": self.current_user.nick_name,
                    "id": self.current_user.id
                }
            except Question.DoesNotExist as e:
                self.set_status(404)
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class QuestionDetailHandler(RedisHandler):
    async def get(self, question_id):
        """获取某个帖子的详情"""
        re_data = {}
        question_details = await self.application.objects.execute(
            Question.extend().where(Question.id == int(question_id)))
        if len(question_details) > 0:
            for data in question_details:
                item_dict = model_to_dict(data)
                re_data = item_dict
        else:
            self.set_status(404)
        self.finish(json.dumps(re_data, default=json_serial))


class QuestionHandler(RedisHandler):
    async def get(self):
        # 获取小组列表
        re_data = []
        question_query = Question.extend()

        # 根据类别进行过滤
        c = self.get_argument('c', None)
        if c:
            question_query = question_query.filter(Question.category == c)
        # 根据参数进行排序
        order = self.get_argument('o', None)
        if order:
            if order == "new":
                question_query = question_query.order_by(Question.add_time.desc())
            elif order == "hot":
                question_query = question_query.order_by(Question.member_nums.desc())

        limit = self.get_argument("limit", None)
        if limit:
            question_query = question_query.limit(int(limit))
        questions = await self.application.objects.execute(question_query)
        for quesion in questions:
            quesion_dict = model_to_dict(quesion)
            quesion_dict["image"] = "{}/media/{}/".format(self.settings["SITE_URL"], quesion_dict["image"])
            re_data.append(quesion_dict)

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self):
        """发帖"""
        re_data = {}
        question_form = QuestionForm(self.request.body_arguments)
        if question_form.validate():
            # 图片验证
            files_meta = self.request.files.get("image", None)
            if not files_meta:
                self.set_status(400)
                re_data["front_image"] = "请上传图片"
            else:
                # 完成验证 通过aiofiles 写文件
                new_filename = ""
                for meta in files_meta:
                    filename = meta['filename']
                    new_filename = "{uuid}_{filename}".format(uuid=uuid.uuid1(), filename=filename)
                    file_path = os.path.join(self.settings['MEDIA_ROOT'], new_filename)
                    async with aiofiles.open(file_path, 'wb') as f:
                        await f.write(meta['body'])
                question = await self.application.objects.create(Question, user=self.current_user,
                                                                 category=question_form.category.data,
                                                                 title=question_form.title.data,
                                                                 content=question_form.content.data,
                                                                 image=new_filename)
                re_data['id'] = question.id
        else:
            self.set_status(400)
            for field in question_form.errors:
                re_data[field] = question_form.errors[field][0]
        self.finish(re_data)
