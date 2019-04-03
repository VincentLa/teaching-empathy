from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.SignUp, name='signup'),
    path('topics/', views.topics, name='topics'),
    path('notifications/', views.notifications, name='notifications'),
    path('allconversations/', views.allconversations, name='allconversations'),
    path('profile', views.profile, name = 'profile'),
    path('conversation/<int:pk>', views.conversation, name = 'conversation'),
]