from aip import AipFace
import base64

from pypinyin import lazy_pinyin, Style


class BaiDuFace:
    # 注册应用有的
    def __init__(self, APP_ID='7433682', API_KEY='FNzOrvxFKoGfihDzA6PbSm8Z', SECRET_KEY='PPFMJButV8pxEwRw2MkrfQloyb2pQTlc'):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipFace(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    # 注册人脸
    def add_user(self, file_obj, userId):
        # 把图片转成base64
        image = base64.b64encode(file_obj.read()).decode('utf-8')
        imageType = "BASE64"
        groupId = "smart_1"
        # userId = "dilireba" # 用人名拼音
        """ 调用人脸注册 """
        # client.addUser(image, imageType, groupId, userId);

        """ 如果有可选参数 """
        options = {}
        options["user_info"] = userId
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["action_type"] = "REPLACE"
        """ 带参数调用人脸注册 """
        res = self.client.addUser(image, imageType, groupId, userId, options)

        return res

    # 删除人脸
    def delete(self, userId, faceToken):
        groupId = "smart_1"
        """ 调用人脸删除 """
        res = self.client.faceDelete(userId, groupId, faceToken)
        return res

    # 搜索人脸
    def search(self, file_obj):
        image = base64.b64encode(file_obj.read()).decode('utf-8')
        imageType = "BASE64"
        groupIdList = "smart_1"
        """ 调用人脸搜索 """
        res = self.client.search(image, imageType, groupIdList)
        return res

    # 人名转拼音
    def name_to_pinyin(self, text):
        style = Style.TONE3
        name_list = lazy_pinyin(text, style=style)
        return ''.join(name_list)


# 语音识别
class BaiDuVoice:
    def __init__(self, APP_ID='', API_KEY='', SECRET_KEY=''):
        """ 你的 APPID AK SK """
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipSpeech(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def speed(self, voice_object):
        res = self.client.asr(voice_object.read(), 'pcm', 16000, {
            'dev_pid': 1537,
        })

        return res

# if __name__ == '__main__':
#     ai=BaiDuVoice()
#     obj=open('./a.wav','rb')
#     res=ai.speed(obj)
#     # {'corpus_no': '7361805862129187193', 'err_msg': 'success.', 'err_no': 0, 'result': ['你好你好，欢迎进入我们社区。'], 'sn': '884103912761714053997'}
#     print(res)
