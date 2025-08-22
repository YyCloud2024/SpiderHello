from django.urls import path
from BloodSpiderAPI.apis.user import request

urlpatterns = [
    path('create/', request.create_user_identity, name='create_user_identity'),
    path('delete/', request.delete_user_identity, name='delete_user_identity'),
    path('update/', request.update_user_identity, name='update_user_identity'),
    path('get/', request.get_user_identity, name='get_user_identity'),
    path('search/', request.search_user_identities, name='search_user_identities'),
    path('toggle_status/', request.toggle_user_identity_status, name='toggle_user_identity_status'),
]