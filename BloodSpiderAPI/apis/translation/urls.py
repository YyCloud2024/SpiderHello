from BloodSpiderAPI.apis.translation import m_youdao_com
from django.urls import path, include

# api/translation/
urlpatterns = [
    # 翻译接口
    path('m_youdao_com_translate/', m_youdao_com.m_youdao_com_translate),
    # 获取翻译语言
    path('m_youdao_com_get_language/', m_youdao_com.m_youdao_com_get_language),
]