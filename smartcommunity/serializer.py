from rest_framework import serializers
from .models import Banner, Notice, Collection, Area


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = '__all__'


class CollectionSerializer(serializers.ModelSerializer):  # 查询所有的序列化类
    class Meta:
        model = Collection
        fields = ['id', 'name', 'avatar', 'area']
        depth = 1  # area 外键关联详情拿到


class CollectionSaveSerializer(serializers.ModelSerializer):  # 新增数据的序列化类
    class Meta:
        model = Collection
        fields = ['name', 'avatar', 'area']

    # 重写create方法完成保存
    def create(self, validated_data):
        instance = super().create(validated_data)
        return instance


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['id', 'name', 'desc']
