from django.urls import path
from . import views
urlpatterns = [
    path('',views.item_create,name='item_create'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('item/<int:item_id>/update/', views.item_update, name='item_update'),
    path('item/list', views.item_list_view, name='item_list'),
    path('item/stock/<int:item_id>/', views.item_stock_view, name='item_stock_view'),
    path('item/search/', views.search_form, name='search_form'),
    path('searchresult/', views.search_results, name='search_results'),


    path('itemreceipt/create', views.itemreceipt_create, name='itemreceipt_create'),
    path('itemreceipt/update/<int:pk>/', views.itemreceipt_update, name='itemreceipt_update'),
    path('itemreceipt/list/', views.itemreceiptinfo_list, name='itemreceiptinfo_list'),
    path('itemreceipt/delete/<int:pk>/', views.itemreceiptinfo_delete, name='itemreceiptinfo_delete'),
    
    
    path('itemdelivery/create', views.itemdelivery_create, name='itemdelivery_create'),
    path('itemdelivery/update/<int:pk>/', views.itemdelivey_update, name='itemdelivey_update'),
    path('itemdelivery/list/', views.itemdeliveryinfo_list, name='itemdeliveryinfo_list'),
    path('itemdelivery/delete/<int:pk>/', views.itemdeliveryinfo_delete, name='itemdeliveryinfo_delete'),
    
    path('salesorder/create/', views.salesorder_create, name='salesorder_create'),
    path('salesorder/update/<int:pk>/', views.salesorder_update, name='salesorder_update'),
    path('salesorder/list/', views.salesorder_info_list, name='salesorder_info_list'),
    path('salesorder/delete/<int:pk>/', views.salesorder_info_delete, name='salesorder_info_delete'),
    
    path('warehouses/create/', views.warehouse_create, name='warehouse_create'),
    path('currency/create/', views.currency_create, name='currency_create'),
    path('unit/create/', views.unit_create, name='unit_create'),


    path('business_partner/create/', views.business_partner_create, name='business_partner_create'),

    path('stock/create/', views.stock_create, name='stock_create'),


]