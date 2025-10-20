# podcasts/serializers.py
from rest_framework import serializers
from .models import Creator, Channel, Episode


class CreatorSerializer(serializers.ModelSerializer):
    """크리에이터 시리얼라이저"""
    class Meta:
        model = Creator
        fields = ['id', 'name', 'bio', 'email', 'created_at']
        read_only_fields = ['id', 'created_at']


class ChannelSerializer(serializers.ModelSerializer):
    """채널 시리얼라이저"""
    creator_name = serializers.CharField(source='creator.name', read_only=True)

    class Meta:
        model = Channel
        fields = [
            'id', 'creator', 'creator_name', 'title',
            'description','thumbnail', 'category', 'is_active', 'created_at'
        ]
        read_only_fields = ['id', 'creator_name', 'created_at']

class EpisodeSerializer(serializers.ModelSerializer):
    """에피소드 시리얼라이저"""
    channel_title = serializers.CharField(source='channel.title', read_only=True)

    class Meta:
        model = Episode
        fields = [
            'id', 'channel', 'channel_title', 'title', 'description','audio_file', 'is_published','published_at', 'created_at'
        ]
        read_only_fields = ['id', 'channel_title', 'published_at', 'created_at']

########################################################

# 간단한 에피소드 시리얼라이저 (Nested용)
class EpisodeSimpleSerializer(serializers.ModelSerializer):
    """Nested용 간단한 에피소드 시리얼라이저"""
    class Meta:
        model = Episode
        fields = ['id', 'title', 'description', 'is_published', 'published_at', 'created_at']


# 채널 목록용 시리얼라이저
class ChannelListSerializer(serializers.ModelSerializer):
    """채널 목록 조회용 (가벼운 버전)"""
    creator_name = serializers.CharField(source='creator.name', read_only=True)
    episode_count = serializers.IntegerField(source='episodes.count', read_only=True)

    class Meta:
        model = Channel
        fields = [
            'id', 'title', 'creator_name', 'category',
            'episode_count', 'is_active'
        ]


# 채널 상세용 시리얼라이저
class ChannelDetailSerializer(serializers.ModelSerializer):
    """채널 상세 조회용 (전체 에피소드 포함)"""
    creator_name = serializers.CharField(source='creator.name', read_only=True)
    episodes = EpisodeSimpleSerializer(many=True, read_only=True)  # ⭐ 조회 전용!

    class Meta:
        model = Channel
        fields = [
            'id', 'creator', 'creator_name', 'title', 'description',
            'category', 'is_active', 'created_at', 'episodes'
        ]