from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ChannelViewSet, EpisodeViewSet, stream_audio, AuthViewSet
router = DefaultRouter()
router.register(r'users', UserViewSet,basename='user')
router.register(r'channels', ChannelViewSet,basename='channel')
router.register(r'episodes', EpisodeViewSet,basename='episode')
router.register(r'auth', AuthViewSet,basename='auth')
urlpatterns = [
    path('', include(router.urls)),
    path('episodes/<int:pk>/stream/', stream_audio, name='stream_audio'),
]

# serializer 추가
# viewset 추가
# url 추가
# python manage.py runserver
# drf web 화면을 사용하여 조회 및 생성 진행 - 크리에이터, 채널, 에피소드 샘플 데이터 입력
# 11:10까지 진행 보겠습니다!