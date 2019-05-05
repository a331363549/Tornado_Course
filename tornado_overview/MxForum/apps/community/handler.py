import uuid

from MxForum.MxForm.handler import RedisHandler
# 用戶是否已登录
from MxForum.apps.community.models import CommunityGroup
from MxForum.apps.utils.mxform_decorators import authenticated_async
from MxForum.apps.community.forms import CommunityGroupForm

import aiofiles
import os


class GroupHandler(RedisHandler):
    # @authenticated_async
    async def get(self):
        self.request.headers.get("tsessionid", None)
        pass

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
                                                              from_image=new_filename)

                re_data['id'] = group.id
        else:
            self.set_status(400)
            for field in group_form.errors:
                re_data[field] = group_form.errors[field][0]
        self.finish(re_data)
