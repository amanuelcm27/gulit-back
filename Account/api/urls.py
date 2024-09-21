from django.urls import path
from .views import *


urlpatterns = [
    path('login/', main_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('csrf-token/', csrf_token_view, name='csrf_token'),
    path('get_user/', get_logged_in_user ,name ="get_user"),
    path('sign_with_google/',login_with_google, name='sign_with_google')
]