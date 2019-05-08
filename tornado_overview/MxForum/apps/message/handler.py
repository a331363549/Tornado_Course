import json

from MxForum.MxForm.handler import RedisHandler
# 用戶是否已登录
from MxForum.apps.message.models import *
from MxForum.apps.utils.mxform_decorators import authenticated_async





class MessageHandler(RedisHandler):
    @authenticated_async
    async def get(self):
        """获取当前登录用户的消息"""
        re_data = []
        type_list = self.get_query_arguments("message_type", [])
        if type_list:
            message_query = Message.filter(Message.receiver_id == self.current_user.id,
                                           Message.message_type.in_(type_list))
        else:
            message_query = Message.filter(Message.receiver_id == self.current_user.id)
        messages = await self.application.objects.execute(message_query)
        for message in messages:
            # 另一种使用外键获取User信息的方式
            sender = await self.application.objects.get(User, id=message.sender_id)
            url=""
            re_data.append({
                "sender": {
                    "id": sender.id,
                    "nick_name": sender.nick_name,
                    "head_url": "/media/" + url if sender.head_url else "",
                },
                "message": message.message,
                "message_type": message.message_type,
                "parent_content": message.parent_content,
                "add_time": message.add_time.strftime("%Y-%m-%d %H:%M:%S")
            })

        self.finish(json.dumps(re_data))
