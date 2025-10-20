# podcasts/validators.py (새로 생성)
from django.core.exceptions import ValidationError

def validate_audio_file_extension(value):
    """오디오 파일 확장자 검증 (.mp3만 허용)"""
    import os
    ext = os.path.splitext(value.name)[1]  # 파일 확장자 추출
    valid_extensions = ['.mp3']

    if ext.lower() not in valid_extensions:
        raise ValidationError('MP3 파일만 업로드 가능합니다.')


def validate_audio_file_size(value):
    """오디오 파일 크기 검증 (100MB 이하)"""
    filesize = value.size  # 바이트 단위
    max_size_mb = 100
    max_size_bytes = max_size_mb * 1024 * 1024  # MB → 바이트 변환

    if filesize > max_size_bytes:
        raise ValidationError(f'파일 크기는 {max_size_mb}MB 이하여야 합니다.')


def validate_image_file_extension(value):
    """이미지 파일 확장자 검증 (.jpg, .png만 허용)"""
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.jpg', '.jpeg', '.png']

    if ext.lower() not in valid_extensions:
        raise ValidationError('JPG 또는 PNG 파일만 업로드 가능합니다.')


def validate_image_file_size(value):
    """이미지 파일 크기 검증 (5MB 이하)"""
    filesize = value.size
    max_size_mb = 5
    max_size_bytes = max_size_mb * 1024 * 1024

    if filesize > max_size_bytes:
        raise ValidationError(f'이미지 크기는 {max_size_mb}MB 이하여야 합니다.')
