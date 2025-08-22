
from django.urls import path
from BloodSpiderAPI.apis.virtual_emails.minmail_app import request

# /api/virtual_emails/minmail_app/
urlpatterns = [
    path("create/", request.create_email),
    path("get/", request.get_email),
]
