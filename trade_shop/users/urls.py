from django.urls import path
from users import views

urlpatterns = [
    path("", views.profile, name="profile"),
    path("login/", views.login_user, name="login"),
    path("logout/", views.logout_user, name="logout"),
]