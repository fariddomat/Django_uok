from django.urls import path
from .views import register, home, predict, prediction_result_view
from .views import manage_universities, create_university, update_university, delete_university
from .views import manage_specifications, create_specification, update_specification, delete_specification
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/', register, name='register'),
    path('', home, name='home'),
    path('predict/', predict, name='predict'),
    path('predict/result/<int:prediction_id>/', prediction_result_view, name='prediction_result_view'),

    path('universities/', manage_universities, name='manage_universities'),
    path('universities/create/', create_university, name='create_university'),
    path('universities/update/<int:pk>/', update_university, name='update_university'),
    path('universities/delete/<int:pk>/', delete_university, name='delete_university'),

    path('specifications/', manage_specifications, name='manage_specifications'),
    path('specifications/create/', create_specification, name='create_specification'),
    path('specifications/update/<int:pk>/', update_specification, name='update_specification'),
    path('specifications/delete/<int:pk>/', delete_specification, name='delete_specification'),

    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Add this line
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),  # Ensure 'home' or any other page is your homepage


]
