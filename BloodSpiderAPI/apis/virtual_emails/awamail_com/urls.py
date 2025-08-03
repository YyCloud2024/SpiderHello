
from django.urls import path
from BloodSpiderAPI.apis.virtual_emails.awamail_com import request

# /api/virtual_emails/awamail_com/
urlpatterns = [
    path("create/", request.create_email),
    path("get/", request.get_email),
]
