from django.shortcuts import render


# index
def index(request):
    return render(request, template_name='pc/index.html')


# 音乐页面
def music_index(request):
    return render(request, template_name='pc/页面/音乐页面/首页.html')

# 视频解析
def video_analysis_index(request):
    return render(request, template_name='pc/页面/视频解析/首页.html')

# 虚拟邮箱
def virtual_emails_index(request):
    return render(request, template_name='pc/页面/虚拟邮箱/首页.html')

# 翻译
def translation_index(request):
    return render(request, template_name='pc/页面/翻译/首页.html')

# AI音视频处理
def ai_audio_video_processing_index(request):
    return render(request, template_name='pc/页面/音视频处理/首页.html')

