from django.db import models
from podcasts.models import Episode

# Create your models here.
class PlayLog(models.Model):
    """
    오디오 재생 기록
    
    사용 예시:
    - 가장 인기 있는 에피소드 파악
    - 사용자별 청취 이력
    - 재생 시간대 분석
    """
    episode = models.ForeignKey(
        Episode, 
        on_delete=models.CASCADE,
        related_name='play_logs'
    )
    
    # IP 주소로 사용자 식별 (로그인 기능 없어도 됨)
    ip_address = models.GenericIPAddressField()
    
    # 재생 시작 시각
    played_at = models.DateTimeField(auto_now_add=True)
    
    # User-Agent (어떤 브라우저/기기에서 들었는지)
    user_agent = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-played_at']  # 최근 재생이 먼저
        
    def __str__(self):
        return f"{self.episode.title} - {self.played_at}"