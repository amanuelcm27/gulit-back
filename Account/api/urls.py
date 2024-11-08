from django.urls import path
from .views import *
from .views import *

urlpatterns = [
    path('login/', main_login, name='login'),
    path('logout/', logout_user, name='logout'),
    path('csrf-token/', csrf_token_view, name='csrf_token'),
    path('get_user/', get_logged_in_user ,name ="get_user"),
    path('sign_with_google/',login_with_google, name='sign_with_google'),
    path('register/', register , name='register'),
    path('set_role/<int:pk>/', SetUserRoleView.as_view() , name='set_role'),
    path('create_customer_profile/', CreateCustomerProfileView.as_view() , name='create_customer_profile'),
    path('update_customer_profile/<int:pk>/', UpdateCustomerProfileView.as_view() , name='update_customer_profile'),
    path('get_customer_profile/', CustomerProfileView.as_view() , name='get_customer_profile'),
]