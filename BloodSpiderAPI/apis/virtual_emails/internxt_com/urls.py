
from django.urls import path
from BloodSpiderAPI.apis.virtual_emails.internxt_com import request

# /api/virtual_emails/internxt_com/
urlpatterns = [
    path("create/", request.create_email),
    path("get/", request.get_email),
]
