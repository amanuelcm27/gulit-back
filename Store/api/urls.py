from django.urls import path
from .views import *


urlpatterns = [
    path('test/',test_view,name='test_view')
]