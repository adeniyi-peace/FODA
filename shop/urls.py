from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    path('food/<int:food_id>/', views.food_detail, name='detail'),
]
