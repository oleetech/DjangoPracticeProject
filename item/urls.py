from django.urls import path
from . import views
urlpatterns = [
    path('',views.item_create,name='item_create'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/update/', views.item_update, name='item_update'),

    path('item/list', views.item_list_view, name='item_list'),
    path('item/stock/<int:item_id>/', views.item_stock_view, name='item_stock_view'),
    path('warehouses/create/', views.warehouse_create, name='warehouse_create'),
    path('currency/create/', views.currency_create, name='currency_create'),
    path('unit/create/', views.unit_create, name='unit_create'),


    path('business_partner/create/', views.business_partner_create, name='business_partner_create'),
    path('item/search/', views.search_form, name='search_form'),
    path('searchresult/', views.search_results, name='search_results'),


]