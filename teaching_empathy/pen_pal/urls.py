from django.urls import path
from django.urls import include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('topics/', views.topics, name='topics'),
    path('signup/', views.SignUp.as_view(), name='signup'),
]