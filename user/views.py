from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout

from .forms import EditUserForm, Addressform
from .models import Address

# Create your views here.

class DashboardView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "")
    

class EditUserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        form = EditUserForm(instance=user)

        context = {
            "form":form,
        }
        
        return render(request, "", context=context)
    
    def post(self, request):
        user = request.user
        form = EditUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            messages.success(request, "Your have succefully edited Your profile")

            return redirect(reverse("dashboard"))

        context = {
            "form":form,
        }
        
        return render(request, "", context=context)
    

class DeleteUserProfileView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user
        logout(request)
        user.delete()
        messages.success(request, "Your have succefully deleted Your account")
        return redirect(reverse(""))
    



class AddressView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, "")


class AddAddressView(LoginRequiredMixin, View):
    def get(self, request):
        form = Addressform()

        context = {
            "form":form
        }

        return render(request, "", context)

    def post(self, request):
        form = Addressform(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.user = request.user
            form.save()

            messages.success(request, "New address has been added")

            return redirect()

        context = {
            "form":form
        }

        return render(request, "", context)


# Note: change Address.objects.get(pk=pk) so that it will relate directly
#  to the user in session, as of now another user can access another's address
#  by typing the link on the search bar directly
class EditAddressView(LoginRequiredMixin, View):
    def get(self, request, pk):
        model = Address.objects.get(pk=pk)
        form = Addressform(instance=model)

        context = {
            "form":form
        }

        return render(request, "", context)

    def post(self, request, pk):
        model = Address.objects.get(pk=pk)
        form = Addressform(request.POST, instance=model)

        if form.is_valid():
            form.save()

            messages.success(request, "Your have succefully edited Your Address")

            return redirect()

        context = {
            "form":form
        }

        return render(request, "", context)
    

class DeleteAddressView(LoginRequiredMixin, View):
    def get(self, request, pk):
        model = Address.objects.get(pk=pk)
        model.delete()

        messages.success(request, "Your address has been deleted")

        return redirect()