from django.urls import path
from .views import (
    home, detail, posts, create_post, latest_posts,
    search_result, profile_view)  # Import the profile_view function from views module

urlpatterns = [
    path("", home, name="home"),
    path("detail/<slug>/", detail, name="detail"),
    path("posts/<slug>/", posts, name="posts"),
    path("create_post", create_post, name="create_post"),
    path("latest_posts", latest_posts, name="latest_posts"),
    path("search", search_result, name="search_result"),
    path('profile/', profile_view, name='profile'),  # Use profile_view directly
    path('detail/<slug:slug>/',detail, name='detail'),
]