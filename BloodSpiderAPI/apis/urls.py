
from django.urls import path, include

urlpatterns = [
    # 音乐接口
    path('music/', include('BloodSpiderAPI.apis.music.urls')),
    # 第三方工具
    path('utils/', include('BloodSpiderAPI.apis.utils.urls')),
    # 虚拟邮箱
    path('virtual_emails/', include('BloodSpiderAPI.apis.virtual_emails.urls')),
]
