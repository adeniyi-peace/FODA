from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, InvalidPage

from .models import Food

from vendor.utils import get_current_day_and_time
from vendor.models import Vendor
# Create your views here.




def index(request):
    context ={
         'mesage':'somethongS'
     }
    return render(request, 'index.html', context)


def shop(request):
    context = {
        'message': 'Welcome to the Food Delivery App!',
        'food_items': Food.objects.all()
    }
    return render(request, 'shop.html', context)

def food_detail(request, food_id):
    try:
        food_item = Food.objects.get(id=food_id)
    except Food.DoesNotExist:
        return render(request, '404.html', status=404)

    context = {
        'food_item': food_item
    }
    return render(request, 'detail.html', context)

def vendors_list(request):
    day, time = get_current_day_and_time()
    model = Vendor.objects.all()
    
    paginator = Paginator(model, 1)

    page_number = request.GET.get("page")

    try:
        vendors = paginator.get_page(page_number)
    except EmptyPage:
        vendors = paginator.get_page(paginator.num_pages)
    except InvalidPage:
        vendors = paginator.get_page(1)
    
    context = {
        "vendors":vendors
    }

    return render(request, "shop/vendors_list.html", context)

def vendor_food_list(request, slug):
    # vendor = get_object_or_404(Vendor, slug=slug)
    # food = vendor.foods.all()

    context = {
        # "vendor":vendor,
        # "food":food,
    }

    return render(request, "shop/vendor_food_list.html", context)