# podcasts/views.py
from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Creator, Channel, Episode
from .serializers import (
    CreatorSerializer,
    ChannelSerializer,
    EpisodeSerializer,
    ChannelListSerializer,
    ChannelDetailSerializer,
)

class CreatorViewSet(viewsets.ModelViewSet):
    """크리에이터 ViewSet"""
    queryset = Creator.objects.all()
    serializer_class = CreatorSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['name', 'bio', 'email']
    ordering_fields = ['created_at', 'name']
    ordering = ['-created_at']


class ChannelViewSet(viewsets.ModelViewSet):
    """채널 ViewSet (최적화 버전)"""
    # queryset = Channel.objects.all()  # queryset 추가
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['creator', 'category', 'is_active']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    ordering = ['-created_at']
    serializer_class = ChannelListSerializer

    def get_queryset(self):
        """액션에 따른 쿼리 최적화"""
        queryset = Channel.objects.all()
        
        # 상세 조회 시 에피소드 prefetch
        #  prefetch_related를 적용하면 쿼리 성능이 향상됩니다.
        # 과연, 이 부분에서 이게 효과가 있는가??        
        if self.action == 'retrieve':
            queryset = queryset.prefetch_related('episodes')
        
        # FK 관계 최적화
        return queryset.select_related('creator')
    
    def get_serializer_class(self):
        """액션에 따른 시리얼라이저 분기"""
        if self.action == 'retrieve':
            return ChannelDetailSerializer
        elif self.action == 'list':
            return ChannelListSerializer
        return ChannelSerializer


class EpisodeViewSet(viewsets.ModelViewSet):
    """에피소드 ViewSet"""
    queryset = Episode.objects.all()
    serializer_class = EpisodeSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['channel', 'is_published']
    search_fields = ['title', 'description']
    ordering_fields = ['published_at', 'created_at']
    ordering = ['-published_at']


# 1시 20분까지 실습해 보겠습니다.
# 새롭게 적용한 Nested 시리얼라이저 적용 및 조회 진행
# 내용이 우리가 적용한 방식으로 표시되는지 확인