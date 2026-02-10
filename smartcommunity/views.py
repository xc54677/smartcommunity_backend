from django.shortcuts import render
from django.http import JsonResponse

from libs.baidu_ai import BaiDuFace
from smartcommunity.models import Welcome, Banner


# 广告接口--》比较low--》使用fbv写的--》后期一般不会这么写
def welcome(request):
    # 1 查出order最大的一张图片，返回给前端
    res = Welcome.objects.all().order_by('-order').first()
    # print("welcome url: " + res.img.url)
    # img = 'http://192.168.2.8:8000/media/' + str(res.img)
    img = request.build_absolute_uri(res.img.url)
    return JsonResponse({'code': 100, 'msg': '成功', 'result': img})


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from .models import Banner, Notice
from .serializer import BannerSerializer, NoticeSerializer, CollectionSerializer, CollectionSaveSerializer


class BannerView(GenericViewSet, ListModelMixin):
    queryset = Banner.objects.filter(is_delete=False).order_by('order')[:3]
    serializer_class = BannerSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        # 获取最后一条通知
        notice = Notice.objects.all().order_by('create_time').first()
        serializer = NoticeSerializer(instance=notice)

        return Response({'code': 100, 'msg': '成功', 'banner': res.data, 'notice': serializer.data})


from .models import Collection
from datetime import datetime
from rest_framework.mixins import DestroyModelMixin, CreateModelMixin


# 信息采集接口--》查询登录用户当天采集的所有数据(未完成-还没写登录，暂时先查当天所有采集的数据)
class CollectionView(GenericViewSet, ListModelMixin, DestroyModelMixin, CreateModelMixin):
    # 查出当天的-->>没过滤当前用户
    queryset = Collection.objects.all().filter(create_time__gte=datetime.now().date())
    serializer_class = CollectionSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CollectionSaveSerializer
        else:
            return CollectionSerializer

    def list(self, request, *args, **kwargs):
        res = super().list(request, *args, **kwargs)
        today_count = len(self.get_queryset())
        return Response({'code': 100, 'msg': '成功', 'result': res.data, 'today_count': today_count})

    ## 删除人脸
    def destroy(self, request, *args, **kwargs):
        from libs.baidu_ai import BaiDuFace
        instance = self.get_object()
        # 百度ai中删除
        baidu = BaiDuFace()
        res = baidu.delete(instance.name_pinyin, instance.face_token)
        self.perform_destroy(instance)
        return Response()


from .models import Area
from .serializer import AreaSerializer


# 查询当前用户负责的网格，目前拿所有的
class AreaView(GenericViewSet, ListModelMixin):
    queryset = Area.objects.all()
    serializer_class = AreaSerializer


from django.db.models import Count
from django.db.models.functions import Trunc
from .models import Collection
from .serializer import StatisticsListSerializer


## 采集统计
class StatisticsView(GenericViewSet, ListModelMixin):
    # 做个分组
    queryset = Collection.objects.annotate(date=Trunc('create_time', 'day')).values('date').annotate(
        count=Count('id')).values('date', 'count')
    serializer_class = StatisticsListSerializer


# 人脸检测接口  post请求
class FaceView(GenericViewSet, ListModelMixin):
    def create(self, request, *args, **kwargs):
        # 1 取出前端传入的人脸照片
        avatar_object = request.data.get('avatar')
        if not avatar_object:
            return Response({'code': 103, 'msg': '请正常提交人脸'})
        # 2 使用百度人脸库--》搜索
        ai = BaiDuFace()
        res = ai.search(avatar_object)
        if res.get('error_code') == 0:
            # 3 查到了，取出userid--》能匹配成功多个，咱们只取第一条
            user_id = res.get('result').get('user_list')[0].get('user_id')
            score = int(res.get('result').get('user_list')[0].get('score'))
            # 4 去咱们采集库，查出用户详情
            user = Collection.objects.filter(name_pinyin=user_id).first()
            return Response({'code': 100, 'msg': '匹配成功', 'name': user.name, 'score': score})
        else:
            return Response({'code': 102, 'msg': '该人员不是咱们社区人员，请注意'})


### 语音识别
from libs.baidu_ai import BaiDuVoice


class VoiceView(GenericViewSet):
    def create(self, request, *args, **kwargs):
        voice_object = request.data.get('voice')
        # with open('./a.wav','wb') as f:
        #     f.write(voice_object.read())
        ai = BaiDuVoice()
        result = ai.speed(voice_object)
        # {'corpus_no': '6847771638436561158', 'result': ['你是不是打过来？'], 'sn': '15921476781594371078', 'err_msg': 'success.', 'err_no': 0}
        if result.get('err_no') == 0:
            return Response({'code': 100, 'msg': '识别成功', 'result': result.get('result')})
        else:
            return Response({'code': 101, 'msg': '识别失败'})


# 公告接口
from .models import Notice
from .serializer import NoticeSerializer


class NoticeView(GenericViewSet, ListModelMixin):
    queryset = Notice.objects.all().order_by('-create_time')
    serializer_class = NoticeSerializer


## 活动接口
from .models import Activity
from .serializer import ActivitySerializer


class ActivityView(GenericViewSet, ListModelMixin):
    queryset = Activity.objects.all().order_by('date')
    serializer_class = ActivitySerializer
