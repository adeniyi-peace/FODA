from django.urls import path
from . import views

urlpatterns = [
    path("dashboard/", views.DashboardView.as_view(), name="dashboard"),

    path("dashboard/edit-profile/", views.EditUserProfileView.as_view(), name="edit_profile"),
    path("dashboard/delete-profile/", views.DeleteUserProfileView.as_view(), name="delete_profile"),

    path("dashboard/addresses/", views.AddressView.as_view(), name="dashboard"),
    path("dashboard/addresses/add-address/", views.AddAddressView.as_view(), name="add_address"),
    path("dashboard/addresses/edit-address/<int:pk>", views.EditAddressView.as_view(), name="edit_address"),
    path("dashboard/addresses/delete-address/<int:pk>", views.DeleteAddressView.as_view(), name="delete_address"),
]
