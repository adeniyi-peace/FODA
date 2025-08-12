from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.vendor_signup_view, name="register"),
    path("login/", views.vendor_login_view, name="vendor_login"),
]
