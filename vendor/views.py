from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django import forms # Import forms module for ModelForm
from django.db.models import Sum, Count, F
from django.db.models.functions import TruncDay, TruncMonth
import json
from datetime import timedelta
from django.utils import timezone

# Import your models based on the new structure
from user.models import User
from vendor.models import Vendor
from products.models import Product, ProductCategory
from orders.models import Order, OrderItem

# --- Helper function to check if user is a vendor ---
def is_vendor_user(user):
    """
    Checks if the logged-in user has an associated Vendor profile and
    their user_type is set to 'vendor'.
    This is crucial for restricting access to vendor-specific dashboards.
    """
    return user.is_authenticated and hasattr(user, 'vendor_profile') and user.user_type == 'vendor'

# --- Vendor Dashboard Home View ---
@login_required # Ensures only logged-in users can access
@user_passes_test(is_vendor_user, login_url='/accounts/login/?next=/vendor-dashboard/') # Redirects non-vendors
def vendor_dashboard_home(request):
    """
    Displays the main vendor dashboard with an overview of their shops,
    total products, total sales, and recent orders.
    """
    # Access the Vendor object associated with the logged-in User
    vendor_obj = request.user.vendor_profile
    # Get all shops owned by this vendor
    vendor_shops = vendor_obj.shops.all()

    # Calculate total products across all shops owned by the vendor
    total_products = Product.objects.filter(shop__in=vendor_shops).count()

    # Calculate total sales (revenue) for all products sold from the vendor's shops
    # Filters OrderItems where the associated Product belongs to one of the vendor's shops
    # and the Order status is 'completed'.
    total_sales = OrderItem.objects.filter(
        product__shop__in=vendor_shops,
        order__status='completed'
    ).aggregate(total_revenue=Sum(F('quantity') * F('price_at_purchase')))['total_revenue']

    # Handle case where there are no sales yet
    if total_sales is None:
        total_sales = 0

    # Fetch recent orders that contain products from the vendor's shops
    # .distinct() is used to avoid duplicate orders if an order contains multiple
    # items from the same vendor's shops.
    recent_orders = Order.objects.filter(
        items__product__shop__in=vendor_shops
    ).distinct().order_by('-order_date')[:5] # Limit to 5 recent orders

    context = {
        'vendor': vendor_obj,
        'vendor_shops': vendor_shops,
        'total_products': total_products,
        'total_sales': total_sales,
        'recent_orders': recent_orders,
    }
    return render(request, 'vendors_dashboard/dashboard_home.html', context)

# --- Product Management Forms ---
class ProductForm(forms.ModelForm):
    """
    Form for creating and updating Product instances.
    It filters the 'shop' queryset to only show shops belonging to the current vendor.
    """
    class Meta:
        model = Product
        fields = ['shop', 'name', 'description', 'price', 'category', 'image', 'is_available']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}), # Make description a larger text area
        }

    def __init__(self, *args, **kwargs):
        # Pop the 'vendor' instance passed from the view
        self.vendor = kwargs.pop('vendor', None)
        super().__init__(*args, **kwargs)
        if self.vendor:
            # Limit the 'shop' dropdown choices to only shops owned by the current vendor
            self.fields['shop'].queryset = Shop.objects.filter(vendor=self.vendor).order_by('name')
        # Ensure categories are ordered for better UX
        self.fields['category'].queryset = ProductCategory.objects.all().order_by('name')


# --- Product Management (CRUD Operations) ---

class VendorProductListView(ListView):
    """
    Displays a list of all products belonging to the logged-in vendor's shops.
    """
    model = Product
    template_name = 'vendors_dashboard/product_list.html'
    context_object_name = 'products' # Name of the variable in the template context

    @user_passes_test(is_vendor_user, login_url='/accounts/login/?next=/vendor-dashboard/products/')
    def dispatch(self, request, *args, **kwargs):
        # This method is called before get_queryset, ensuring authorization
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Filter the queryset to only include products from the current vendor's shops
        vendor_obj = self.request.user.vendor_profile
        vendor_shops = vendor_obj.shops.all()
        return Product.objects.filter(shop__in=vendor_shops).order_by('-created_at')

class VendorProductCreateView(CreateView):
    """
    Handles the creation of new products for the logged-in vendor's shops.
    """
    model = Product
    form_class = ProductForm # Use the custom form to filter shops
    template_name = 'vendors_dashboard/product_create.html'
    success_url = reverse_lazy('vendor_product_list') # Redirect after successful creation

    @user_passes_test(is_vendor_user, login_url='/accounts/login/?next=/vendor-dashboard/products/add/')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_form_kwargs(self):
        """
        Pass the current vendor object to the form's __init__ method
        so it can filter the 'shop' queryset.
        """
        kwargs = super().get_form_kwargs()
        kwargs['vendor'] = self.request.user.vendor_profile
        return kwargs

    def form_valid(self, form):
        # The form's 'shop' field is already restricted to the vendor's shops,
        # so no explicit assignment of vendor/shop is needed here beyond what the form handles.
        return super().form_valid(form)

class VendorProductUpdateView(UpdateView):
    """
    Handles updating existing products belonging to the logged-in vendor's shops.
    """
    model = Product
    form_class = ProductForm
    template_name = 'vendors_dashboard/product_update.html'
    success_url = reverse_lazy('vendor_product_list')

    @user_passes_test(is_vendor_user, login_url='/accounts/login/?next=/vendor-dashboard/products/edit/')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Ensure the vendor can only update products from their own shops
        vendor_obj = self.request.user.vendor_profile
        vendor_shops = vendor_obj.shops.all()
        return Product.objects.filter(shop__in=vendor_shops)

    def get_form_kwargs(self):
        """
        Pass the current vendor object to the form's __init__ method
        so it can filter the 'shop' queryset for updates.
        """
        kwargs = super().get_form_kwargs()
        kwargs['vendor'] = self.request.user.vendor_profile
        return kwargs

class VendorProductDeleteView(DeleteView):
    """
    Handles deleting products belonging to the logged-in vendor's shops.
    """
    model = Product
    template_name = 'vendors_dashboard/product_confirm_delete.html'
    success_url = reverse_lazy('vendor_product_list')

    @user_passes_test(is_vendor_user, login_url='/accounts/login/?next=/vendor-dashboard/products/delete/')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        # Ensure the vendor can only delete products from their own shops
        vendor_obj = self.request.user.vendor_profile
        vendor_shops = vendor_obj.shops.all()
        return Product.objects.filter(shop__in=vendor_shops)

# --- Sales Report and Trends View ---

@login_required
@user_passes_test(is_vendor_user, login_url='/accounts/login/?next=/vendor-dashboard/sales/')
def vendor_sales_report(request):
    """
    Generates and displays sales reports and trends for the logged-in vendor's shops.
    Includes total revenue, monthly/daily sales trends, and top-selling products.
    """
    vendor_obj = request.user.vendor_profile
    vendor_shops = vendor_obj.shops.all()

    # Fetch all completed sales items related to the vendor's shops
    all_sales = OrderItem.objects.filter(
        product__shop__in=vendor_shops,
        order__status='completed'
    ).order_by('order__order_date')

    # Calculate total revenue
    total_revenue = all_sales.aggregate(Sum(F('quantity') * F('price_at_purchase')))['total_revenue'] or 0

    # Calculate Sales by Month for trend analysis
    sales_by_month = all_sales.annotate(month=TruncMonth('order__order_date')).values('month').annotate(
        total_sales=Sum(F('quantity') * F('price_at_purchase'))
    ).order_by('month')

    # Prepare data for Chart.js (monthly sales)
    monthly_labels = [s['month'].strftime('%Y-%m') for s in sales_by_month]
    monthly_data = [float(s['total_sales']) for s in sales_by_month]

    # Calculate Sales by Day for the last 30 days (trend analysis)
    today = timezone.now()
    thirty_days_ago = today - timedelta(days=30)

    sales_last_30_days = all_sales.filter(order__order_date__gte=thirty_days_ago).annotate(
        day=TruncDay('order__order_date')
    ).values('day').annotate(
        total_sales=Sum(F('quantity') * F('price_at_purchase'))
    ).order_by('day')

    # Prepare data for Chart.js (daily sales)
    daily_labels = [s['day'].strftime('%Y-%m-%d') for s in sales_last_30_days]
    daily_data = [float(s['total_sales']) for s in sales_last_30_days]

    # Identify Top Selling Products by quantity and revenue
    top_selling_items = all_sales.values('product__name').annotate(
        total_quantity_sold=Sum('quantity'),
        total_revenue_item=Sum(F('quantity') * F('price_at_purchase'))
    ).order_by('-total_quantity_sold')[:5] # Get top 5 products

    context = {
        'total_revenue': total_revenue,
        'sales_by_month_labels': json.dumps(monthly_labels), # Dump to JSON for safe passing to JS
        'sales_by_month_data': json.dumps(monthly_data),
        'sales_by_day_labels': json.dumps(daily_labels),
        'sales_by_day_data': json.dumps(daily_data),
        'top_selling_items': top_selling_items,
    }
    return render(request, 'vendors_dashboard/sales_report.html', context)