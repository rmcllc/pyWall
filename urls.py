from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('validating', views.registerUser),
    path('userValidation', views.validateUser),
    path('myWall', views.myWall),
    path('newPost', views.newPost),
    path('delete/', views.delete_session),
]