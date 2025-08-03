
from django.urls import path, include
# api/utils/
urlpatterns = [
    path("reccloud/", include("BloodSpiderAPI.apis.utils.reccloud.urls"))
]
