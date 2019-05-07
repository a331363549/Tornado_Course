import json
import uuid

from MxForum.MxForm.handler import RedisHandler
# 用戶是否已登录
from MxForum.apps.community.models import *
from MxForum.apps.community.forms import *
from MxForum.apps.utils.mxform_decorators import authenticated_async

import aiofiles
import os
from playhouse.shortcuts import model_to_dict
from MxForum.apps.utils.util_func import json_serial


class LikeHandler(RedisHandler):
    @authenticated_async
    async def post(self, comment_id):
        """点赞"""
        re_data = {}
        try:
            comment = await self.application.objects.get(PostComment, id=int(comment_id))
            comment_like = await self.application.objects.create(CommentLike, user=self.current_user,
                                                                 post_comment=comment)
            comment.like_nums += 1
            await self.application.objects.update(comment)
            re_data['id'] = comment_like.id
        except PostComment.DoesNotExist as e:
            self.set_status(404)
        self.finish(re_data)


class CommentReplayHandler(RedisHandler):
    @authenticated_async
    async def get(self, comment_id):
        """刷新回复消息"""
        re_data = []
        try:
            comment_replys = await self.application.objects.execute(
                PostComment.extend().where(PostComment.parent_comment_id == int(comment_id)))
            for item in comment_replys:
                item_dict = {
                    "user": model_to_dict(item.user),
                    "content": item.content,
                    "reply_nums": item.reply_nums,
                    "add_time": item.add_time.strftime("%Y-%m-%d"),
                    "id": item.id
                }
                re_data.append(item_dict)
        except PostComment.DoesNotExist as e:
            self.set_status(404)
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, comment_id):
        """添加回复"""
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = CommentReplyForm.from_json(param)
        if form.validate():
            try:
                comment = await self.application.objects.get(PostComment, id=int(comment_id))
                replyed_user = await self.application.objects.get(User, id=form.replyed_user.data)

                reply = await self.application.objects.create(PostComment, user=self.current_user,
                                                              parent_comment=comment, replyed_user=replyed_user,
                                                              content=form.content.data)

                # 修改comment的回复数
                comment.reply_nums += 1
                await self.application.objects.update(comment)
                re_data['id'] = reply.id
                re_data["user"] = {
                    "id": self.current_user.id,
                    "nick_name": self.current_user.nick_name
                }

            except User.DoesNotExist as e:
                self.set_status(400)
                re_data["replyed_user"] = "用户不存在"
            except PostComment.DoesNotExist as e:
                self.set_status(404)
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class PostCommentHandler(RedisHandler):
    @authenticated_async
    async def get(self, post_id):
        """获取帖子下的所有评论"""
        re_data = []
        try:
            post = await self.application.objects.get(Post, id=int(post_id))
            post_comments = await self.application.objects.execute(
                PostComment.extend().where(PostComment.post == post, PostComment.parent_comment.is_null(True)).order_by(
                    PostComment.add_time.desc())
            )

            for item in post_comments:
                has_liked = False
                try:
                    comments_like = await self.application.objects.get(CommentLike, post_comment_id=item.id,
                                                                       user_id=self.current_user.id)
                    has_liked = True
                except CommentLike.DoesNotExist as e:
                    pass
                item_dict = {
                    "user": model_to_dict(item.user),
                    "content": item.content,
                    "reply_nums": item.reply_nums,
                    "like_nums": item.like_nums,
                    "has_liked": has_liked,
                    "id": item.id,
                }
                re_data.append(item_dict)
        except Post.DoesNotExist as e:
            self.set_status(404)
        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self, post_id):
        """新增评论"""
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = PostCommentForm.from_json(param)
        if form.validate():
            try:
                post = await self.application.objects.get(Post, id=int(post_id))
                post_comment = await self.application.objects.create(PostComment, post=post, user=self.current_user,
                                                                     content=form.content.data)
                post.comment_nums += 1
                await self.application.objects.update(post)
                re_data["id"] = post_comment.id
                re_data["user"] = {}
                re_data["user"]["nick_name"] = self.current_user.nick_name
                re_data["user"]["id"] = self.current_user.id
            except Post.DoesNotExist as e:
                self.set_status(404)
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class PostDetailHandler(RedisHandler):
    @authenticated_async
    async def get(self, post_id):
        """获取某个帖子的详情"""
        re_data = {}
        post_details = await self.application.objects.execute(Post.extend().where(Post.id == int(post_id)))
        if len(post_details) > 0:
            for data in post_details:
                item_dict = {
                    "user": model_to_dict(data.user),
                    "title": data.title,
                    "content": data.content,
                    "comment_nums": data.comment_nums,
                    "add_time": data.add_time.strftime("%Y-%m-%d")
                }
                re_data = item_dict
        else:
            self.set_status(404)
        self.finish(re_data)


class PostHandler(RedisHandler):
    @authenticated_async
    async def get(self, group_id):
        """获取小组内的帖子"""
        post_list = []
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            group_member = await self.application.objects.get(CommunityGroupMember,
                                                              user=self.current_user,
                                                              community=group,
                                                              status="agree")
            posts_query = Post.extend()
            c = self.get_argument("cate", None)
            if c:
                if c == "hot":
                    posts_query = posts_query.filter(Post.is_hot == True)
                if c == "excellent":
                    posts_query = posts_query.filter(Post.is_excellent == True)
            posts = await self.application.objects.execute(posts_query)
            for post in posts:
                item_dict = {
                    "user": {
                        "id": post.user.id,
                        "nick_name": post.user.nick_name
                    },
                    "id": post.id,
                    "title": post.title,
                    "content": post.content,
                    "comment_nums": post.comment_nums
                }
                post_list.append(item_dict)
        except CommunityGroup.DoesNotExist as e:
            self.set_status(404)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(403)

        self.finish(json.dumps(post_list))

    @authenticated_async
    async def post(self, group_id):
        """发帖"""
        re_data = {}
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            group_member = await self.application.objects.get(CommunityGroupMember,
                                                              user=self.current_user,
                                                              community=group,
                                                              status="agree")
            param = self.request.body.decode("utf8")
            param = json.loads(param)
            form = PostForm.from_json(param)
            if form.validate():
                post = await self.application.objects.create(Post, user=self.current_user,
                                                             title=form.title.data,
                                                             group=group,
                                                             content=form.content.data)
                re_data['id'] = post.id
            else:
                self.set_status(400)
                for field in form.errors:
                    re_data[field] = form.errors[field][0]
        except CommunityGroup.DoesNotExist as e:
            self.set_status(404)
        except CommunityGroupMember.DoesNotExist as e:
            self.set_status(403)
        self.finish(re_data)


class Group_DatilHandler(RedisHandler):
    @authenticated_async
    async def get(self, group_id):
        # 获取小组基本信息
        re_data = {}
        try:
            group = await self.application.objects.get(CommunityGroup, id=int(group_id))
            item_dict = {}
            item_dict["name"] = group.name
            item_dict["id"] = group.id
            item_dict["desc"] = group.desc
            item_dict["notice"] = group.notice
            item_dict["member_nums"] = group.member_nums
            item_dict["post_nums"] = group.post_nums
            item_dict["front_image"] = "{}/media/{}/".format(self.settings["SITE_URL"], group.front_image)
            re_data = item_dict
        except CommunityGroup.DoesNotExist as e:
            self.set_status(404)
        self.finish(re_data)


class GroupMemberHandler(RedisHandler):
    @authenticated_async
    async def post(self, group_id):
        # 申请加入小组
        re_data = {}
        param = self.request.body.decode("utf8")
        param = json.loads(param)
        form = GroupApplyForm.from_json(param)
        if form.validate():
            try:
                group = await self.application.objects.get(CommunityGroup, id=int(group_id))
                existend = await self.application.objects.get(CommunityGroupMember, community=group,
                                                              user=self.current_user)
                self.set_status(400)
                re_data["non_fields"] = "用户已加入"
            except CommunityGroup.DoesNotExist as e:
                self.set_status(404)
            except CommunityGroupMember.DoesNotExist as e:
                community_member = await self.application.objects.create(CommunityGroupMember,
                                                                         community=group,
                                                                         user=self.current_user,
                                                                         apply_reason=form.apply_reason)
                re_data['id'] = community_member.id
        else:
            self.set_status(400)
            for field in form.errors:
                re_data[field] = form.errors[field][0]
        self.finish(re_data)


class GroupHandler(RedisHandler):
    async def get(self):
        # 获取小组列表
        re_data = []
        community_query = CommunityGroup.extend()

        # 根据类别进行过滤
        c = self.get_argument('c', None)
        if c:
            community_query = community_query.filter(CommunityGroup.category == c)
        # 根据参数进行排序
        order = self.get_argument('o', None)
        if order:
            if order == "new":
                community_query = community_query.order_by(CommunityGroup.add_time.desc())
            elif order == "hot":
                community_query = community_query.order_by(CommunityGroup.member_nums.desc())

        limit = self.get_argument("limit", None)
        if limit:
            community_query = community_query.limit(int(limit))
        groups = await self.application.objects.execute(community_query)
        for group in groups:
            group_dict = model_to_dict(group)
            group_dict["front_image"] = "{}/media/{}/".format(self.settings["SITE_URL"], group_dict["front_image"])
            re_data.append(group_dict)

        self.finish(json.dumps(re_data, default=json_serial))

    @authenticated_async
    async def post(self):
        re_data = {}
        # 不能使用jsonform
        group_form = CommunityGroupForm(self.request.body_arguments)
        if group_form.validate():
            # 图片字段的验证自己完成
            files_meta = self.request.files.get("front_image", None)
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
                group = await self.application.objects.create(CommunityGroup,
                                                              creator=self.current_user,
                                                              name=group_form.name.data,
                                                              category=group_form.category.data,
                                                              desc=group_form.desc.data,
                                                              notice=group_form.notice.data,
                                                              front_image=new_filename)

                re_data['id'] = group.id
        else:
            self.set_status(400)
            for field in group_form.errors:
                re_data[field] = group_form.errors[field][0]
        self.finish(re_data)
