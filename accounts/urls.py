from django.urls import path
from .import views


urlpatterns=[
    path("github/login/", views.github_login, name="github_login"),
    path("github/callback/", views.github_callback, name="github_callback"),
    path("logout/", views.logout_view, name="logout"),
]