from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum, F, Prefetch
from django.db.models.functions import TruncDay, TruncMonth
from datetime import timedelta
from django.utils import timezone
from django.contrib import messages
import json

from .utils import hash_password
from django.http import HttpResponse
from .utils import check_password
from shop.models import OrderItem, Food, Order
from .models import Vendor, BusinessHour
from .forms import BusinessHourFormSet, FoodForm


def v_signup(request):
    if request.method == "POST":
        
        email = request.POST["email"]
        password = request.POST["password"]

        if Vendor.objects.filter(email=email).exists():
            return render(request, "v_signup.html", {"error": "Email already taken"})

        hashed_pw = hash_password(password)
        Vendor.objects.create(email=email, password=hashed_pw)

        return redirect(reverse("vendor_login"))

    return render(request, "v_signup.html")


def v_login(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        try:
            user = Vendor.objects.get(email=email)
            if check_password(password, user.password):
                request.session["user_id"] = user.id  # 🔑 store session
                return redirect("vendor_dashboard")
            else:
                return HttpResponse("Invalid password")
        except Vendor.DoesNotExist:
            return HttpResponse("User not found")

    return render(request, "v_login.html")

def logout(request):
    request.session.flush()
    return redirect("v_login")



# def is_vendor_user(user):
#     return user.is_authenticated and hasattr(user, 'vendor') and user.user_type == 'vendor'


# @login_required
# @user_passes_test(is_vendor_user, login_url='/auth/login/?next=/vendor-dashboard/')
def vendor_dashboard(request):
    if not request.vendor_user:
        return redirect(reverse("vendor_login"))
   
    vendor = request.vendor_user

    # Food items created by the vendor
    vendor_foods = Food.objects.filter(vendor=vendor)
    
    total_foods = vendor_foods.count()

    # Total revenue and order items related to vendor
    order_items = OrderItem.objects.filter(vendor=vendor)

    total_sales = order_items.aggregate(
        total_revenue=Sum(F('quantity') * F('price'))
    )['total_revenue'] or 0

    # Sales by month
    sales_by_month = order_items.annotate(
        month=TruncMonth('order__order_date')
    ).values('month').annotate(
        total_sales=Sum(F('quantity') * F('price'))
    ).order_by('month')

    monthly_labels = [s['month'].strftime('%Y-%m') for s in sales_by_month]
    monthly_data = [float(s['total_sales']) for s in sales_by_month]

    # Sales by day (last 30 days)
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)

    sales_last_30_days = order_items.filter(
        order__order_date__gte=thirty_days_ago
    ).annotate(
        day=TruncDay('order__order_date')
    ).values('day').annotate(
        total_sales=Sum(F('quantity') * F('price'))
    ).order_by('day')

    daily_labels = [s['day'].strftime('%Y-%m-%d') for s in sales_last_30_days]
    daily_data = [float(s['total_sales']) for s in sales_last_30_days]

    # Top-selling foods
    top_selling_foods = order_items.values('food__name').annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum(F('quantity') * F('price'))
    ).order_by('-total_quantity')[:5]

    context = {
        'vendor': vendor,
        'foods': vendor_foods,
        'orders': order_items,
        'total_foods': total_foods,
        'total_sales': total_sales,
        'sales_by_month_labels': json.dumps(monthly_labels),
        'sales_by_month_data': json.dumps(monthly_data),
        'sales_by_day_labels': json.dumps(daily_labels),
        'sales_by_day_data': json.dumps(daily_data),
        'top_selling_foods': top_selling_foods,
    }
    
    # return render(request, "dashboard.html", {"user": request.vendor_user})
    return render(request, "v_dashboard.html", context)


def vendor_business_hours(request):
    # vendor = get_object_or_404(Vendor, id=4)
    vendor = request.vendor_user
    business_hours = vendor.business_hour.all()

    if request.method == "POST":
        formset = BusinessHourFormSet(
            request.POST, request.FILES, instance=vendor, queryset=business_hours
        )

        if formset.is_valid():
            formset.save()
            messages.success(request, "Schedule Updated Successfully!")
            return redirect(reverse('vendor_dashboard'))
    
    else:
        formset = BusinessHourFormSet(instance=vendor, queryset=business_hours)

    context = {
        "business_hours":business_hours,
        "formset":formset
    }

    return render(request, "vendor/business_hours.html", context=context)
    
def vendor_food_list(request):
    vendor = get_object_or_404(Vendor, id=4)
    # vendor = request.vendor_user
    foods = Food.objects.filter(vendor=vendor)

    if request.method == "POST":
        id = request.POST.get("id","")
        operation = request.POST.get("method", "")
        
        try:
            # add vendor later
            food = Food.objects.get(id=id, vendor=vendor)
            name = food.name

            if operation == "true":
                food.is_sale = True
                food.save()
                return JsonResponse({"success":True, "message":f"{name} is now available in shop"})
            
            elif operation == "false":
                food.is_sale = False
                food.save()
                return JsonResponse({"success":True, "message":f"{name} has been removed from shop"})
            
            else:
                return JsonResponse(
                    {"success":False, "message":f"An error occured while updating {name} availability"}
                )

        except ObjectDoesNotExist:
            return JsonResponse({"success":False, "message":"The food does not exist, reload the page to fix error."})

    context = {
        "foods":foods
    }

    return render(request, "vendor/food_list.html", context=context)

def add_food(request):
    # vendor = request.vendor
    vendor = get_object_or_404(Vendor, id=4)
    form = FoodForm

    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES)

        if form.is_valid():
            form = form.save(commit=False)
            form.vendor = vendor
            form.save()

            messages.success(request, f"The food {form.name} has been Created")

            return redirect("vendor_food_list")

    context = {"form":form}

    return render(request, "vendor/add_food.html", context)

def update_food(request, id):
    # vendor = request.vendor
    vendor = get_object_or_404(Vendor, id=4)
    food = get_object_or_404(Food, id=id, vendor=vendor)
    form = FoodForm(instance=food)

    if request.method == "POST":
        form = FoodForm(request.POST, request.FILES, instance=food)

        if form.is_valid():
            form = form.save(commit=False)
            form.vendor = vendor
            form.save()

            messages.success(request, f"The food {food.name} has been Updated")

            return redirect("vendor_food_list")

    context = {"form":form}

    return render(request, "vendor/update_food.html", context)

def delete_food(request, id):
    # vendor = request.vendor
    vendor = get_object_or_404(Vendor, id=4)
    food = get_object_or_404(Food, id=id, vendor=vendor)

    food.delete()
    messages.success(request, f"The food {food.name} has been deleted suceesfully")
    
    return redirect("vendor_food_list")

def vendor_customer_order(request):
    # vendor = request.vendor
    vendor = get_object_or_404(Vendor, id=4)
    orders = Order.objects.filter(order_item__vendor=vendor).prefetch_related(
        Prefetch("order_item", queryset=OrderItem.objects.select_related("food"))
    )

    if request.method == "POST":
        action = request.POST.get("action","")
        id = request.POST.get("id","")

        item = OrderItem.objects.filter(id=id).first()

        if action == "confirm":
            item.status = "CF"
            item.save()

        elif action == "cancel":
            item.status = "CN"
            item.save()

        elif action == "sent":
            item.status = "ST"
            item.save()

        elif action == "delivered":
            item.status = "DL"
            item.save()

        context = {
            "orders": orders
        }

        html = render_to_string("vendor/includes/order_include.html", context, request)

        return JsonResponse({"html":html})

    context = {
        "orders": orders
    }
    
    
    return render(request, "vendor/customer_orders.html", context)