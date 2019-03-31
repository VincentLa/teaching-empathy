from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('profile', views.profile, name = 'profile'),
    path('conversation/<int:pk>', views.conversation, name = 'conversation'),
]