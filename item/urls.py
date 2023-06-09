from django.urls import path
from . import views
urlpatterns = [
    path('',views.item_create,name='item_create'),
    path('warehouses/create/', views.warehouse_create, name='warehouse_create'),
    path('unit/create/', views.unit_create, name='unit_create'),
     path('business_partner/create/', views.business_partner_create, name='business_partner_create'),
]