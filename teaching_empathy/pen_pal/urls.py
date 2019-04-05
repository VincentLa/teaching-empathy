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
    path('end_phase/<int:pk>', views.end_phase, name='end_phase'),
    path('conversation/<int:pk>', views.conversation, name = 'conversation'),
    path('report/<int:pk>', views.report, name='report'),
]