from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages

from .forms import UnitForm
from .models import Unit

from .models import Currency

from .forms import ItemForm
from .models import Item

from .models import Warehouse
from .forms import WarehouseForm


from .models import BusinessPartner
from .forms import BusinessPartnerForm

def unit_create(request):
    # Retrieve the success message from the query parameters
    success_message = request.GET.get('success_message')
    if request.method == 'POST':
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('unit_create')
    else:
        form = UnitForm()
        

    return render(request, 'item/unit_create.html', {'form': form})


def warehouse_create(request):
    # Retrieve the success message from the query parameters
    success_message = request.GET.get('success_message')
    if request.method == 'POST':
        form = WarehouseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('warehouse_create')
    else:
        form = WarehouseForm()
        

    return render(request, 'item/warehouse_create.html', {'form': form})


def item_create(request):
    warehouses = Warehouse.objects.all()
    units = Unit.objects.all()
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('item_create')
    else:
        warehouses = Warehouse.objects.all()
        units = Unit.objects.all()
        form = ItemForm()
    return render(request, 'item/item_create.html', {'form': form,'warehouses': warehouses,'units':units})

def business_partner_create(request):

    if request.method == 'POST':
        form = BusinessPartnerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('index')
    else:
        currencies = Currency.objects.all()
        form = BusinessPartnerForm()
    return render(request, 'item/business_partner_create.html', {'form': form,'currencies': currencies})

