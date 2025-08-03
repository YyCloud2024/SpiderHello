from BloodSpiderAPI.apis.utils.reccloud import request
from django.urls import path, include

# api/utils/reccloud/
urlpatterns = [
    # 语音转文字 - 创建任务
    path("tastasksks_audio_speech_create/", request.tastasksks_audio_speech_create),
    # 语音转文字 - 查询结果
    path("tastasksks_audio_speech_task_id/", request.tastasksks_audio_speech_task_id),
    # 语音转文字 - 创建任务
    path("tasks_audio_recognition_create/", request.tasks_audio_recognition_create),
    # 语音转文字 - 查询结果
    path("tasks_audio_recognition_task_id/", request.tasks_audio_recognition_task_id),
    # 视频翻译 - 创建任务
    path("tasks_media_video_translation_create/", request.tasks_media_video_translation_create),
    # 视频翻译 - 查询结果
    path("tasks_tasks_media_video_translation_task_id/", request.tasks_tasks_media_video_translation_task_id),
    # 人声分离 - 创建任务
    path("tasks_tasks_media_background_separation_create/", request.tasks_tasks_media_background_separation_create),
    # 人声分离 - 查询结果
    path("tasks_tasks_media_background_separation_task_id/", request.tasks_tasks_media_background_separation_task_id),
    # 上传文件
    path('tasks/file/upload/', request.tasks_file_upload),
]