from django.urls import path
from .views import register, home, predict

urlpatterns = [
    path('register/', register, name='register'),
    path('', home, name='home'),
     path('predict/', predict, name='predict'),
]
