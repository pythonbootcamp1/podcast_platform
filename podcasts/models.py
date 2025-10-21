# podcasts/models.py
from django.db import models
from .validators import validate_image_file_extension, validate_image_file_size, validate_audio_file_extension, validate_audio_file_size
# class Creator(models.Model):
#     """크리에이터 모델 (YouTube 채널 운영자와 같은 개념)"""
#     name = models.CharField(max_length=100)
#     bio = models.TextField(blank=True)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.name

#     class Meta:
#         ordering = ['-created_at']
from django.contrib.auth.models import User

class Channel(models.Model):
    """채널 모델 (YouTube 채널과 같은 개념)"""
    CATEGORY_CHOICES = [
        ('education', '교육'),
        ('entertainment', '엔터테인먼트'),
        ('tech', '기술'),
        ('music', '음악'),
        ('news', '뉴스'),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='channels'  # ⭐ creator.channels로 역참조 가능!
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='channels/', null=True, blank=True,validators=[validate_image_file_extension, validate_image_file_size])
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

class Episode(models.Model):
    """에피소드 모델 (YouTube 비디오와 같은 개념)"""
    channel = models.ForeignKey(
        Channel,
        on_delete=models.CASCADE,
        related_name='episodes'  # ⭐ channel.episodes로 역참조 가능!
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    audio_file = models.FileField(upload_to='episodes/', null=True, blank=True,validators=[validate_audio_file_extension, validate_audio_file_size])
    is_published = models.BooleanField(default=False)
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.channel.title} - {self.title}"

# Channel 모델에 -> thumbnail 필드 추가(ImageField)
# Episode 모델에 -> audio_file 필드 추가(FileField)
# python manage.py makemigrations, python manage.py migrate 실행
# 2:35까지 진행


# drf web 에서 파일 업로드 테스트
# media 폴더에서 확인하기
# db에 저장되는 내용이 http:~~~~의 규칙 확인

# validators를 적용해서 이미지파일과 오디오파일의 검증을 실습해 보겠습니다!
# 3:50까지 해보겠습니다!
