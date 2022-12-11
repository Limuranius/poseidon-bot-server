from django.urls import path, include
from .views import CreateUserView, LoginView

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register_url"),
    path("login/", LoginView.as_view(), name="login_url")
]