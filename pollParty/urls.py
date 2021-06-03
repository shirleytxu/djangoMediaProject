from django.urls import path, include
from . import views

urlpatterns = [
    # URL for Home page
    path('', views.index, name="index"),

    # URL for creating polls
    path('createpoll/', views.AddPostView.as_view(success_url="/"), name="createpoll"),

    # URL for deleting a poll
    path('deletePost/<int:pk>', views.deletepost, name="deletepost"),

    # URL for viewing the details of a poll
    path('postDetails/<int:pk>', views.PostDetailView.as_view(), name="postDetails"),

    # URL for logging in and logging out from Django library
    path('accounts/', include('django.contrib.auth.urls')),

    # URL for upvoting
    path('upVote/<int:pk>/', views.upvote, name="upvote"),

    # URL for downvoting
    path('downVote/<int:pk>/', views.downvote, name="downvote"),

    # URL for registering a new user
    path('accounts/register/', views.register, name="register"),
]
