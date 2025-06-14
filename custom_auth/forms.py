from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm

from user.models import User


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        exclude = ["full_name"]

class LoginForm(AuthenticationForm):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


    # strictly used for the admin
class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ("email",)

# strictly used for the admin
class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email",)