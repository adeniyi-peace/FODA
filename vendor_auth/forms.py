# from django import forms
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

# from vendor.models import Vendor


# class VendorRegistrationForm(UserCreationForm):
#     class Meta:
#         model = Vendor
#         fields = ["email","name","password1", "password2",]

# class VendorSigninForm(AuthenticationForm):
#     username = forms.EmailField(required=True, widget=forms.EmailInput(attrs={"placeholder":"Email"}))
#     password = forms.CharField(required=True, widget=forms.PasswordInput())


# vendor_auth/forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Vendor

class VendorSignUpForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    class Meta:
        model = Vendor
        fields = ('email', 'shop_name')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don’t match")
        return password2

    def save(self, commit=True):
        vendor = super().save(commit=False)
        vendor.set_password(self.cleaned_data["password1"])
        if commit:
            vendor.save()
        return vendor

class VendorLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
