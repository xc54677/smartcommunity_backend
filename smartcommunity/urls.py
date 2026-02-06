from django.contrib import admin
from django.urls import path
from .views import welcome
from rest_framework.routers import SimpleRouter
from .views import BannerView, CollectionView, AreaView

router = SimpleRouter()
router.register('banner', BannerView, 'banner')
router.register('collection', CollectionView, 'collection')
router.register('area', AreaView, 'area')

urlpatterns = [
    # http://127.0.0.1:8000/smartcommunity/welcome/  ---> 就能获取到图片数据
    path('welcome/', welcome),
]
urlpatterns += router.urls
