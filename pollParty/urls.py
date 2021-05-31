from django.contrib import admin
from django.urls import include, path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path('createpoll/', views.createPoll, name="createpoll"),
    path('postDetails/<int:pk>', views.postDetailView.as_view(), name="postDetails")
]
