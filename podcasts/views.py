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
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ranged_response import RangedFileResponse
from analysis.models import PlayLog

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
    @extend_schema(
        summary="채널 목록 조회",
        description="""
        모든 채널 목록을 조회합니다.
        각 채널에는 에피소드 목록이 포함됩니다.
        """,
        tags=["채널"])
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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


# drf specular 설치
# settings.py 설정
# 1. installed_apps 추가
# 2. REST_FRAMEWORK 설정 추가
# 3. SPECTACULAR_SETTINGS 설정 추가
# 4. urls.py 설정 추가
# 5. 테스트 진행
# - urls.py에서 설정한 endpoint 확인
# - api 테스트 수행
# 10:20 까지



# extend_schema 사용법을 익혀보겠습니다
# description 적용
# tags 적용
# summary 적용
# 어떻게 swagger에서 표현되는지 확인
# 10:50까지 실습해 보겠습니다




# 에피소드를 조회하는데, audio url이 표현되는 id를 찾습니다.(샘플로 text만 넣은 데이터가 있을 수 있어서...)
# 조회 결과에서 url을 확인 -> 예시 주소 : http://localhost:8000/media/episodes/Whispers_of_Tomorrow.mp3
# test_audio.html 파일을 생성
# live server 실행
# 브라우저에서 localhost:5500/test_audio.html 접속
# 음악이 재생되는지 확인
# controls이 잘 되는지 확인 - 재생, 일시정지, 타임라인 바, ...(다운로드...)
# 현재 상황을 파악.
# 11:50까지 실습해 보겠습니다.

@api_view(['GET'])
def stream_audio(request, pk):
    """
    오디오 파일을 스트리밍합니다.
    
    Range Request를 지원하여 seek(탐색) 기능이 정상 작동합니다.
    """
    # 1. Episode 객체 가져오기
    episode = get_object_or_404(Episode, pk=pk)
    
    # 2. 파일이 실제로 존재하는지 확인
    if not episode.audio_file:
        return Response(
            {"error": "이 에피소드에는 오디오 파일이 없습니다."},
            status=404
        )

    # ===== 재생 로그 기록 =====
    # 사용자 IP 추출
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]  # 프록시를 거친 경우
    else:
        ip = request.META.get('REMOTE_ADDR')  # 직접 연결
    
    # User-Agent 추출 (어떤 브라우저인지)
    user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    # Range Request인지 확인
    # Range Request는 seek이므로 새로운 재생으로 카운트하지 않음
    range_header = request.META.get('HTTP_RANGE')
    is_range_request = bool(range_header)
    
    # Range Request가 없거나 range가 처음부터 시작하는 경우만 로그 기록
    if not is_range_request or (is_range_request and range_header.startswith('bytes=0-')):
        # 처음 재생할 때만 로그 기록
        PlayLog.objects.create(
            episode=episode,
            ip_address=ip,
            user_agent=user_agent
        )
        print(f"📊 재생 기록: {episode.title} by {ip}")

    # 3. Range Request를 지원하는 응답 생성
    # RangedFileResponse가 자동으로:
    # - Range 헤더 확인
    # - 206 Partial Content 응답
    # - Content-Range 헤더 설정
    response = RangedFileResponse(
        request,
        open(episode.audio_file.path, 'rb'),
        content_type='audio/mpeg'
    )
    
    return response

# stream_audio view를 만들어서 오디오 스트리밍을 실습해 보겠습니다.
# ranged_response 설치
# views.py에서 작성(stream_audio view 작성)
# urls.py에서 설정
# test_audio.html에서 확인
# 1:50까지 실습해 보겠습니다.


# models.py에서 PlayLog 모델 작성 -> podcasts/models.py or 별도의 app을 구성해서 models.py 작성
# stream_audio view에서 PlayLog 모델 작성 -> 저장되는 로직을 작성 ( ex : 처음 재생할 때만 로그 기록)
# 2:50까지 실습해 보겠습니다.
