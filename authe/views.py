<<<<<<< HEAD
from django.shortcuts import render

# Create your views here.
=======
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin

from django.core.mail import send_mail, EmailMultiAlternatives
from django.template import Context
from django.template.loader import get_template

from user.models import User
from .forms import SignUpForm, LoginForm
from foda.settings import EMAIL_HOST_USER


# TBD - NAME OF THE TEMPLATES AND REDIRECTS


class SignUpView(View):
    def get(self, request):
        form = SignUpForm

        context = {
            "form":form
        }

        return render(request, "", context=context)
        

    def post(self, request):
        form = SignUpForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            first_name = form.cleaned_data.get("first_name")

            user = form.save()

            user.generate_verification_code

            htmly = get_template("auth/...html")

            data = {
                "first_name":first_name,
                "verification_code": user.verification_code
            }

            html_content = htmly.render(data)

            subject = "Welcome"

            msg =EmailMultiAlternatives(subject=subject, body=html_content, 
                                        from_email=EMAIL_HOST_USER, to=[email])
            
            msg.attach_alternative(html_content, "text/html")

            msg.send()

            messages.success(request, "Check your email for the confirmation Code")

            # redirects user to authenrication page
            return render(redirect())
        
        context = {
            "form":form
        }

        return render(request, "", context=context)
        



class LoginView(View):
    def get(self, request):
        form = LoginForm

        next_url = request.GET.get("next", "")

        context = {
            "form":form,
            "next":next_url
        }

        return render(request, "", context=context)
        

    def post(self, request):
        form = LoginForm(request.POST)
        next_url= request.POST.get("next", "")

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)

            if user != None:
                # NOte to self, test this error that come from this in the login html
                if user.is_active:
                    login(request, user) 

                    # redirects to previous page the user was in instead of home page
                    if next_url != "":
                        return redirect(next_url)

                    return redirect()

                else:
                    messages.error(request, "Your account is not active. " \
                    "Please check your email for the verification link or code.")
                    
                    return redirect(reverse("verify_email_page")) 
        
        context = {
            "form":form,
            "next":next_url
        }

        return render(request, "", context=context)
        

class EmailAuthenticationView(View):
    def get(self, request):
        return render(request, "")
    
    def post(self, request):
        code = request.POST.get("verification_code","")

        try:
            user = User.objects.get(verification_code=code, is_active=False) 

            if not user.is_verification_code_valid():
                messages.error(request, "The verification code is invalid or has expired. Please request a new one.")
                return render(request, "") 

            user.activate() 

            messages.success(request, "Your account has been successfully activated! You are now logged in.")

            login(request, user)

            return redirect() 

        except User.DoesNotExist:
            messages.error(request, "The verification code is invalid or has expired. Please request a new one.")
            return render(request, "")
        

class LogoutView(View):
    def get(self, request):
        logout(request)

        #back to homepage
        return redirect()


class UserEmailPasswordResetView(SuccessMessageMixin, PasswordResetView):
    email_template_name = "email_password_reset.html"
    template_name = "auth/confirm_email_password_reset.html"
    success_url = reverse_lazy()
    success_message = "We have  emailed you instructions for resetting your password" \
                    "If an account exists with the email you entered. You should recieve them shortly" \
                    "If you don't recieve an email," \
                    "please make sure you have entered the address registered with, and checked your spam folder"

class UserPasswordResetView(SuccessMessageMixin, PasswordResetConfirmView):
    template_name = "auth/reset_password.html"
    success_url = reverse_lazy("login")
    success_message = "Your password has been set.  You may go ahead and log in now."

class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = "auth/password_change.html"
    success_url = reverse_lazy("dashboard")
    success_message = "Your password was changed."
>>>>>>> c81ada65a6be1235afee95ef52afea834f314b08
