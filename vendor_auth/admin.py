# vendor_auth/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Vendor
from .forms import VendorSignUpForm

class VendorAdmin(BaseUserAdmin):
    add_form = VendorSignUpForm
    model = Vendor
    list_display = ("email", "shop_name", "is_staff")
    list_filter = ("is_staff",)
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Info", {"fields": ("shop_name",)}),
        ("Permissions", {"fields": ("is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('email', 'shop_name', 'password1', 'password2'),
        }),
    )
    search_fields = ("email",)
    ordering = ("email",)

admin.site.register(Vendor, VendorAdmin)
