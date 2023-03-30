from django.urls import path
from . import views
from .views import CustomloginView, RegisterPage, CustomLogoutView

urlpatterns = [
    path("login/", CustomloginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(next_page='login'), name="logout"),
    path("register/", RegisterPage.as_view(), name="register")
]
