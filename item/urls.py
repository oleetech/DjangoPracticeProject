from django.urls import path
from . import views
urlpatterns = [
    path('',views.create,name='index'),
    path('warehouses/create/', views.warehouse_create, name='warehouse_create'),

]