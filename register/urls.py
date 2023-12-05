from django.urls import path
from .views import profile, signup, signin, update_profile, logout, view_profile

urlpatterns = [
    path('profile/', profile, name='profile'),
    path("signup/", signup, name="signup"),
    path("signin/", signin, name="signin"),
    path("update_profile/", update_profile, name="update_profile"),
    path("logout/", logout, name="logout"),
    path('profile/<str:username>/', view_profile, name='view_profile')
]