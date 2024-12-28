from django.urls import path

from .views import (
    login,
    signup,
    edit_profile,
    profile,
)

urlpatterns = [
    path("login/", login, name="login"),
    path("signup/", signup, name="signup"),
    path("profile/", profile, name="profile"),
    path("profile/edit/", edit_profile, name="edit_profile"),
]
