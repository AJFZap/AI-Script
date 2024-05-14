from django.urls import path
from django.urls import re_path
from django.views.static import serve
from django.conf import settings
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    re_path(r'^templates/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),

    path('', views.index, name='index'),
    path('login', views.user_login, name='login'),
    path('signup', views.user_signup, name='signup'),
    path('logout', views.user_logout, name='logout'),
    path('scripts', views.all_scripts, name='scripts'),
    path('generate', views.generate_script, name='generate'),
    path('script_details/<int:pk>/', views.script_details, name='script_details'),
    path('delete/<int:pk>/', views.delete_script, name='delete_script'),
    path('verify_account/<uidb64>/<token>', views.activate, name='verify_account'),
    
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_done.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset_password_success/', auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_complete.html"), name='password_reset_complete'),
]