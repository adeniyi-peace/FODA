from django.urls import path
<<<<<<< HEAD

urlpatterns = [
    
=======
from . import views

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('verify/', views.EmailAuthenticationView.as_view(), name='verify_email_page'),
    path("logut/", views.LogoutView.as_view(), name="logout"),

    path("change_password/", views.UserPasswordChangeView.as_view(), name="change_password"),

    path("reset_password/", views.UserEmailPasswordResetView.as_view(), name="password_reset"),
    path("confirm_reset/<uidb64>/<token>", views.UserPasswordResetView.as_view(), name="confirm_reset"),
>>>>>>> c81ada65a6be1235afee95ef52afea834f314b08
]
