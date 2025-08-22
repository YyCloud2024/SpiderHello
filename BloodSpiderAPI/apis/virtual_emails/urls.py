
from django.urls import path, include


# /api/virtual_emails/
urlpatterns = [
    path("awamail_com/", include("BloodSpiderAPI.apis.virtual_emails.awamail_com.urls")),
    path("internxt_com/", include("BloodSpiderAPI.apis.virtual_emails.internxt_com.urls")),
    path("minmail_app/", include("BloodSpiderAPI.apis.virtual_emails.minmail_app.urls")),
]
