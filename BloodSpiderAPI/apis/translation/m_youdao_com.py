from BloodSpiderModel.DjangoResponseTool.response_dict import response_dict
from BloodSpiderAPI.spider.translation.m_youdao_com.m_youdao_com import YoudaoTranslate


m_youdao_com = YoudaoTranslate()


# 翻译接口
def m_youdao_com_translate(request):
    if request.method == "POST":
        text = request.POST.get("text")
        type_language = request.POST.get("type_language", "AUTO")
        result = m_youdao_com.translate(text, type_language)
        return response_dict(data=result, message="翻译成功")


# 获取翻译语言
def m_youdao_com_get_language(request):
    result = m_youdao_com.get_language()
    return response_dict(data=result, message="获取翻译语言成功")