
from django.urls import path
from BloodSpiderWeb.views import request
urlpatterns = [
    # 首页
    path("index/", request.index, name="首页"),
    # 音乐页面
    path("music/", request.music_index, name="音乐"),
    # 视频解析
    path("video/", request.video_analysis_index, name="视频解析"),
    # 虚拟邮箱
    path("virtual_emails/", request.virtual_emails_index, name="虚拟邮箱"),
    # 翻译
    path("translation/", request.translation_index, name="翻译"),
    # 音视频处理
    path("audio_video_processing/", request.ai_audio_video_processing_index, name="音视频处理"),
]
