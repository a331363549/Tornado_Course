from libs.yuntongxun.CCPRestSDK import REST
# import ConfigParse

_accountSid = "8aaf0708697b6beb0169c1f12db32e2a"
_acountToken = "de035b92fdd448d19729797cdbbc3ef4"
_appId = "8aaf0708697b6beb0169c1f12e082e30"
_serverIP = "sandboxapp.cloopen.com"
# 说明：请求地址，生产环境配置成app.cloopen.com
_serverPort = "8883"
_softVersion = "2013-12-26"


class _CPP(object):
    def __init__(self):
        self.rest = REST(_serverIP, _serverPort, _softVersion)
        self.rest.setAccount(_accountSid, _acountToken)
        self.rest.setAppId(_appId)

    @classmethod
    def instance(cls):
        if not hasattr(cls, "_instance"):
            cls._instance = cls()
        return cls._instance

    def sendTemplateSMS(self, to, datas, tempId):
        return self.rest.sendTemplateSMS(to, datas, tempId)


ccp = _CPP.instance()

if __name__ == '__main__':
    ccp.sendTemplateSMS('18565607772', ["5555", 5], 1)
