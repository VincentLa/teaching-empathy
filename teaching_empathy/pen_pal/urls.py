from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('profile', views.profile, name = 'profile'),
    path('conversation/<int:pk>', views.conversation, name = 'conversation'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]