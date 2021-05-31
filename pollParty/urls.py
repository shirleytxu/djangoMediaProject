from django.contrib import admin
from django.urls import include, path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="index"),
    path('createpoll/', views.AddPostView.as_view(success_url="/"), name="createpoll"),
    path('postDetails/<int:pk>', views.PostDetailView.as_view(), name="postDetails"),
    path('accounts/', include('django.contrib.auth.urls')),

]
