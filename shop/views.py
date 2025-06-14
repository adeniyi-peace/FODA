from django.shortcuts import render
from .models import Food
# Create your views here.

def index(request):
    context = {
        'message': 'Welcome to the Food Delivery App!',
        'food_items': Food.objects.all()
    }
    return render(request, 'index.html', context)