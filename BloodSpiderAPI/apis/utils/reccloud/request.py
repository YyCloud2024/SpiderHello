from BloodSpiderAPI.spider.utils.reccloud_cn.main import ReccloudMain
import json
import os
from django.conf import settings

reccloud = ReccloudMain()

from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict

# AI 文件上传 - 新接口
def tasks_file_upload(request):
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")
    file = request.FILES.get("file")
    if not file:
        return response_dict(code=400, message="缺少必要参数 'file'")
    temp_file_path = settings.MEDIA_ROOT + "/tmp/" + file.name
    try:
        # 保存临时文件

        with open(temp_file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        uploader = reccloud.reccloud_utils.reccloud_upload

        # 上传文件
        upload_result = uploader.upload_file_to_reccloud(temp_file_path)

        if upload_result["success"]:
            return response_dict(message="文件上传成功", data=upload_result["data"])
        else:
            return response_dict(code=500, message=upload_result["message"])
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")
    finally:
        # 删除临时文件
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)


# AI 文字转语音 - 创建任务
def tastasksks_audio_speech_create(request):
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")
    text = request.POST.get("text")
    if not text:
        return response_dict(code=400, message="缺少必要参数 'text'")
    try:
        task_response = reccloud.stasksks_audio_speech(text)
        if task_response is None:
            return response_dict(code=500, message="任务创建失败，请稍后重试")
        return response_dict(message="创建任务成功,正在转换中", data=task_response)
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")

# AI 文字转语音 - 查询结果
def tastasksks_audio_speech_task_id(request):
    if request.method != "GET":
        return response_dict(code=405, message="请求方法错误，仅支持GET请求")
    task_id = request.GET.get("task_id")
    if not task_id:
        return response_dict(code=400, message="缺少必要参数 'task_id'")
    try:
        result = reccloud.tasks_audio_speech_task_id(task_id)
        if result is None:
            return response_dict(code=500, message="查询结果失败，请稍后重试")
        return response_dict(message="查询结果成功", data=result)
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")

# AI 语音转文字 - 创建任务
def tasks_audio_recognition_create(request):
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")
    uniqid = request.POST.get("uniqid")
    if not uniqid:
        return response_dict(code=400, message="缺少必要参数 'uniqid'")
    try:
        task_response = reccloud.tasks_audio_recognition(uniqid)
        if task_response is None:
            return response_dict(code=500, message="任务创建失败，请稍后重试")
        return response_dict(message="创建任务成功,正在处理中", data=task_response)
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")

# AI 语音转文字 - 查询结果
def tasks_audio_recognition_task_id(request):
    if request.method != "GET":
        return response_dict(code=405, message="请求方法错误，仅支持GET请求")
    task_id = request.GET.get("task_id")
    if not task_id:
        return response_dict(code=400, message="缺少必要参数 'task_id'")
    try:
        result = reccloud.tasks_audio_recognition_task_id(task_id)
        if result is None:
            return response_dict(code=500, message="查询结果失败，请稍后重试")
        return response_dict(message="查询结果成功", data=result)
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")

# AI 视频翻译 - 创建任务
def tasks_media_video_translation_create(request):
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")
    try:
        data = json.loads(request.body)
        uniqid = data.get("uniqid")
        voice = data.get("voice", "AvaMultilingual")
        origin_lang = data.get("origin_lang", "zh")
        target_lang = data.get("target_lang", "en")
        if not uniqid:
            return response_dict(code=400, message="缺少必要参数 'uniqid'")
        task_response = reccloud.tasks_media_video_translation_create(uniqid, voice, origin_lang, target_lang)
        if task_response is None:
            return response_dict(code=500, message="任务创建失败，请稍后重试")
        return response_dict(message="创建任务成功,正在处理中", data=task_response)
    except json.JSONDecodeError:
        return response_dict(code=400, message="请求体不是有效的JSON格式")
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")

# AI 视频翻译 - 查询结果
def tasks_tasks_media_video_translation_task_id(request):
    if request.method != "GET":
        return response_dict(code=405, message="请求方法错误，仅支持GET请求")
    task_id = request.GET.get("task_id")
    if not task_id:
        return response_dict(code=400, message="缺少必要参数 'task_id'")
    try:
        result = reccloud.tasks_tasks_media_video_translation_task_id(task_id)
        if result is None:
            return response_dict(code=500, message="查询结果失败，请稍后重试")
        return response_dict(message="查询结果成功", data=result)
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")

# AI 人声分离 - 创建任务
def tasks_tasks_media_background_separation_create(request):
    if request.method != "POST":
        return response_dict(code=405, message="请求方法错误，仅支持POST请求")
    upload_url = request.POST.get("upload_url")
    if not upload_url:
        return response_dict(code=400, message="缺少必要参数 'upload_url'")
    try:
        task_response = reccloud.tasks_tasks_media_background_separation_create(upload_url)
        if task_response is None:
            return response_dict(code=500, message="任务创建失败，请稍后重试")
        return response_dict(message="创建任务成功,正在处理中", data=task_response)
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")

# AI 人声分离 - 查询结果
def tasks_tasks_media_background_separation_task_id(request):
    if request.method != "GET":
        return response_dict(code=405, message="请求方法错误，仅支持GET请求")
    task_id = request.GET.get("task_id")
    if not task_id:
        return response_dict(code=400, message="缺少必要参数 'task_id'")
    try:
        result = reccloud.tasks_tasks_media_background_separation_task_id(task_id)
        if result is None:
            return response_dict(code=500, message="查询结果失败，请稍后重试")
        return response_dict(message="查询结果成功", data=result)
    except Exception as e:
        return response_dict(code=500, message=f"服务器内部错误: {str(e)}")