from BloodSpiderAPI.apis.utils.video_analysis import doyin_request, blbl_request
from django.urls import path, include

# api/utils/video_analysis/
urlpatterns = [
    path("doyin/video_analysis/", doyin_request.video_analysis),
    path("blbl/video_analysis/", blbl_request.video_analysis)
]