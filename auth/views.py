from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages

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

            htmly = get_template("auth/...html")

            data = {
                "first_name":first_name
            }

            html_content = htmly.render(data)

            subject = "Welcome"

            msg =EmailMultiAlternatives(subject=subject, body=html_content, 
                                        from_email=EMAIL_HOST_USER, to=[email])
            
            msg.attach_alternative(html_content, "text/html")

            msg.send()

            messages.success(request, "Check your email for the confirmation Code")

            # login user immediately after signup
            login(request, user)
            
            return render(redirect())
        
        context = {
            "form":form
        }

        return render(request, "", context=context)
        



class LoginView(View):
    def get(self, request):
        form = LoginForm

        next = request.GET.get("next", "")

        context = {
            "form":form,
            "next":next
        }

        return render(request, "", context=context)
        

    def post(self, request):
        form = LoginForm(request.POST)
        next = request.POST.get("next", "")

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, username=email, password=password)

            if user != None:
                login(request, user)

                # redirects to previous page the user was in instead of home page
                if next != "":
                    return redirect(next)

                return redirect()
        
        context = {
            "form":form,
            "next":next
        }

        return render(request, "", context=context)
        
