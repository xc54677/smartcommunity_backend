from django.contrib import admin
from django.urls import path
from rest_framework.routers import SimpleRouter
from .views import welcome, BannerView, CollectionView, AreaView, StatisticsView, FaceView, VoiceView, NoticeView, ActivityView

router = SimpleRouter()
router.register('banner', BannerView, 'banner')
router.register('collection', CollectionView, 'collection')
router.register('area', AreaView, 'area')
router.register('statistics', StatisticsView, 'statistics')
router.register('face', FaceView, 'face')
router.register('voice', VoiceView, 'voice')
router.register('notice', NoticeView, 'notice')
router.register('activity', ActivityView, 'activity')

urlpatterns = [
    # http://127.0.0.1:8000/smartcommunity/welcome/  ---> 就能获取到图片数据
    path('welcome/', welcome),
]
urlpatterns += router.urls
