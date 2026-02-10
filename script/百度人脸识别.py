from aip import AipFace
import base64


class BaiDuFace:
    # 注册应用有的
    def __init__(self, APP_ID='7433682', API_KEY='FNzOrvxFKoGfihDzA6PbSm8Z',
                 SECRET_KEY='PPFMJButV8pxEwRw2MkrfQloyb2pQTlc'):
        self.APP_ID = APP_ID
        self.API_KEY = API_KEY
        self.SECRET_KEY = SECRET_KEY
        self.client = AipFace(self.APP_ID, self.API_KEY, self.SECRET_KEY)

    def add_user(self):
        # 把图片转成base64
        image = base64.b64encode(open('./dlrb2.png', 'rb').read()).decode('utf-8')
        imageType = "BASE64"
        groupId = "smart_1"
        userId = "dilireba"  # 用人名拼音
        """ 调用人脸注册 """
        # client.addUser(image, imageType, groupId, userId);

        """ 如果有可选参数 """
        options = {}
        options["user_info"] = "这是迪丽热巴"
        options["quality_control"] = "NORMAL"
        options["liveness_control"] = "LOW"
        options["action_type"] = "REPLACE"
        """ 带参数调用人脸注册 """
        res = self.client.addUser(image, imageType, groupId, userId, options)

        return res

    # 删除人脸
    def delete(self):
        userId = "dilireba"
        groupId = "smart_1"
        faceToken = "b8d786a717af9bf966fd63d01e8c4be4"
        """ 调用人脸删除 """
        res = self.client.faceDelete(userId, groupId, faceToken)
        return res

    # 搜索人脸
    def search(self):
        image = base64.b64encode(open('./gtl2.png', 'rb').read()).decode('utf-8')
        imageType = "BASE64"
        groupIdList = "smart_1"
        """ 调用人脸搜索 """
        res = self.client.search(image, imageType, groupIdList)
        return res


if __name__ == '__main__':
    ai = BaiDuFace()
    # res = ai.add_user()
    # # 'face_token': 'b8d786a717af9bf966fd63d01e8c4be4'
    # print(res)

    # res = ai.delete()
    # print(res)

    res = ai.search()
    print(res)
