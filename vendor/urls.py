from django.urls import path
from . import views

urlpatterns = [
    path('v_signup/', views.v_signup, name='vendor_signup'),
    path('v_login/', views.v_login, name='vendor_login'),
    path('v_dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path("open-hours/", views.vendor_business_hours, name="buisness_hours" ),
    path("foods/", views.vendor_food_list, name="vendor_food_list"),
    path("foods/add-food/", views.add_food, name="add_food"),
    path("foods/update-food/<int:id>/", views.update_food, name="update_food"),
    path("foods/delete-food/<int:id>/", views.delete_food, name="delete_food"),
    path("orders/", views.vendor_customer_order, name="vendor_orders"),
]
