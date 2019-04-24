import os
from handlers import Passport, VerifyCode, Profile, House, Orders
from handlers.BaseHandler import StaticFileBaseHandler as StaticFileHandler

handlers = [
    (r'/api/register$', Passport.RegisterHandler),  # 註冊
    (r'/api/login$', Passport.LoginHandler),  # 登陸
    (r'/api/logout$', Passport.LogoutHandler),  # 登出
    (r'/api/check_login$', Passport.CheckLoginHandler),  # 檢驗登陸狀態
    (r'/api/profile$', Profile.ProfileHandler),  # 個人信息
    (r'/api/profile/avatar$', Profile.AvatarHandler),  # 頭像
    (r'/api/profile/name$', Profile.NameHandler),  # 用戶名
    (r'/api/profile/auth$', Profile.AuthHandler),  # 實名認證
    (r'/api/imagecode$', VerifyCode.ImageCodeHandler),  # 圖片驗證碼
    (r'/api/smscode$', VerifyCode.SMSCodeHandler),  # 短信驗證碼

    (r'/api/house/area', House.AreaInfoHandler),  # 城區信息
    (r'/api/house/info$', House.HouseInfoHandler),  # 上傳房屋的基本信息
    (r'/api/house/image$', House.HouseIMageHandler),  # 上傳房屋圖片
    (r'/api/house/my$', House.MyHousesHandler),  # 查詢用戶發布的房源
    (r'/api/house/index$', House.IndexHandler),  # 首頁
    (r'/api/house/list$', House.HouseListHandler),  # 房屋過濾列表數據
    (r'/api/house/list2$', House.HouseListRedisHandler),  # 房屋過濾列表數據
    (r'/api/order$', Orders.OrderHandler),  # 下單
    (r'/api/order/my$', Orders.MyOrdersHandler),  # 我的订单,房東房客同時適用
    (r'/api/order/accept$', Orders.OrderCommentHandler),  # 接受订单
    (r'/api/order/reject$', Orders.RejectOrderHandler),  # 拒绝接单
    (r'/api/order/comment$', Orders.OrderCommentHandler),  # 评论

    (r'/(.*)', StaticFileHandler,
     dict(path=os.path.join(os.path.dirname(__file__), "html"), default_filename="index.html"))
]
