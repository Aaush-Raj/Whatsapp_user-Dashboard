from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('userlist/', views.userlist, name='playlist'),
    path('notifications/', views.notifications, name='notifications'),
    path('settings/', views.settings, name='settings'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('newuser/', views.new_user, name='newuser'),
    path('createuser', views.create_user, name='createuser'),
    path('districts/', views.get_districts, name='districts'),
    path('updateuser/<str:user_id>/', views.update_user, name='updateuser'),
]
