from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages


from .forms import ItemForm
from .models import Item
from .models import Warehouse
from .forms import WarehouseForm



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


def create(request):
    warehouses = Warehouse.objects.all()
 
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            
            return redirect('index')
    else:
        warehouses = Warehouse.objects.all()

        form = ItemForm()
    return render(request, 'item/create.html', {'form': form,'warehouses': warehouses})


