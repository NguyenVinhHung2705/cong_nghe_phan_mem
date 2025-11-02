from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # http://localhost:8000/user/register
    path('login/', views.login, name='login'),  # http://localhost:8000/user/login
    path('logout/', views.logout_view, name='logout'),
    path('profile', views.profile, name='profile'),
    path('dang_ky_ban_hang/', views.dang_ky_ban_hang, name='dang_ky_ban_hang'),
    path('khu_vuc_ban_hang/', views.khu_vuc_ban_hang , name='khu_vuc_ban_hang'),
    path('export/<int:user_id>/', views.export_profile_pdf, name='export_profile'),
]