from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('register', views.register_view, name='register_view'),
    path('login', views.login_view, name='login_view'),
    path('login/', views.login_view, name='login_view'),
    path('logout', views.logout_view, name='logout_view'),
    # path('channel/<int:user_id>', views.channel_view, name='channel_view'),
]