from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # http://localhost:8000/user/register
    path('login/', views.login, name='login'),  # http://localhost:8000/user/login
    path('forgot_password/', views.forgot_password, name='forgot_password'),  # http://localhost:8000/user/forgot_password
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('export/<int:user_id>/', views.export_profile_pdf, name='export_profile'),
]