from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.spider.utils.video_analysis import doyin


video_analysis_doyin = doyin.DouyinVideoParse()


# 视频解析
def video_analysis(request):
    try:
        shared_link = request.GET.get('shared_link')
        if shared_link:
            result = video_analysis_doyin.analysis(shared_link)
            return response_dict(data=result, message="解析成功")
        else:
            return response_dict(message="请输入视频链接", code=1)
    except Exception as e:
        return response_dict(code=1, message=f"服务器内部错误: {str(e)}")
