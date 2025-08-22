from BloodSpiderAPI.apis.utils.video_analysis import doyin_request, blbl_request, kuaisho_request, xiaohoshu
from django.urls import path, include

# api/utils/video_analysis/
urlpatterns = [
    path("douyin/video_analysis/", doyin_request.video_analysis),
    path("blbl/video_analysis/", blbl_request.video_analysis),
    path("kuaisho/video_analysis/", kuaisho_request.video_analysis),
    path("xiaohoshu/video_analysis/", xiaohoshu.video_analysis),
]