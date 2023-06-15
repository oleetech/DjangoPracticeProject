from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse



from django.forms import formset_factory, inlineformset_factory
from .models import ItemReceipt, ItemReceiptinfo
from .forms import ItemReceiptinfoForm,ItemReceiptForm


from django.contrib import messages
from django.db.models import Q

from .forms import UnitForm
from .models import Unit

from .forms import CurrencyForm
from .models import Currency


from .forms import ItemForm,SearchForm
from .models import Item

from .models import Warehouse
from .forms import WarehouseForm


from .models import BusinessPartner
from .forms import BusinessPartnerForm

from django.db.models import Sum
from .models import  Stock, ItemReceipt, ItemDelivery




def currency_create(request):
    # Retrieve the success message from the query parameters
    success_message = request.GET.get('success_message')
    if request.method == 'POST':
        form = CurrencyForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('currency_create')
    else:
        form = UnitForm()
        

    return render(request, 'item/currency/currency_create.html', {'form': form})

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
        

    return render(request, 'item/unit/unit_create.html', {'form': form})


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
        

    return render(request, 'item/warehouse/warehouse_create.html', {'form': form})


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
            error_messages = form.errors.values()
            for message in error_messages:
                messages.error(request, message)        
    else:
        warehouses = Warehouse.objects.all()
        units = Unit.objects.all()
        form = ItemForm()
    
    return render(request, 'item/item_create.html', {'form': form,'warehouses': warehouses,'units':units})

def item_update(request, item_id):
    item = get_object_or_404(Item, pk=item_id)
    warehouses = Warehouse.objects.all()
    units = Unit.objects.all()
    
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, 'The item has been updated successfully.')
            return redirect('item_detail', pk=item.id)
    else:
        form = ItemForm(instance=item)
    
    return render(request, 'item/item_create.html', {'form': form, 'item': item, 'warehouses': warehouses, 'units': units})

def search_form(request):

    form = SearchForm(request.POST)
    context = {
        'form': form,
    }
    return render(request, 'item/search_form.html',context)
    
def search_results(request):
    name = request.GET.get('name')
    description = request.GET.get('description')

    results = Item.objects.filter(
        Q(name__icontains=name) 
        # Add more conditions for other columns as necessary
    )
    if results.count() == 1:
        item = results.first()
        form = ItemForm(instance=item)
        return render(request, 'item/item_detail.html', {'form': form, 'item': item})

    return render(request, 'item/search_results.html', {'results': results})

def item_detail(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm(instance=item)
    return render(request, 'item/item_detail.html', {'form': form,'item': item})


def item_list_view(request):
    items = Item.objects.all()

    context = {
        'items': items,
    }

    return render(request, 'item/item_list.html', context)


def item_stock_view(request, item_id):
    item = Item.objects.get(id=item_id)
    warehouses = Warehouse.objects.all()

    


    item_quantities = []
    for warehouse in warehouses:
        stock_quantity = Stock.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0
        receipt_quantity = ItemReceipt.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0
        delivery_quantity = ItemDelivery.objects.filter(warehouse=warehouse, item=item).aggregate(Sum('quantity'))['quantity__sum'] or 0

        total_quantity = stock_quantity + receipt_quantity - delivery_quantity

        item_quantities.append({
            'warehouse': warehouse,
            'quantity': total_quantity,
        })

    context = {
        'item': item,
        'item_quantities': item_quantities,

        
    }

    return render(request, 'item/item_detail_stock.html', context)


def business_partner_create(request):
    if request.method == 'POST':
        form = BusinessPartnerForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The post has been created successfully.')
            return redirect('business_partner_create')
    else:
        currencies = Currency.objects.all()
        form = BusinessPartnerForm()
    return render(request, 'item/business_partner/business_partner_create.html', {'form': form,'currencies': currencies})

def itemreceipt_create(request):
    ItemReceiptFormSet = inlineformset_factory(
        ItemReceiptinfo,
        ItemReceipt,
        form=ItemReceiptForm,
        fields=('item', 'quantity'),
        extra=1,
        can_delete=False,
        min_num=1,
        validate_min=True
    )

    if request.method == 'POST':
        form = ItemReceiptinfoForm(request.POST)
        formset = ItemReceiptFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            # Get the last inserted ItemReceiptinfo
            last_item_receiptinfo = ItemReceiptinfo.objects.last()

            # Calculate the new docno
            if last_item_receiptinfo:
                new_docno = last_item_receiptinfo.docno + 1
            else:
                new_docno = 1
           
            # Save the form with the new docno
            itemreceiptinfo = form.save(commit=False)
            itemreceiptinfo.docno = new_docno
            itemreceiptinfo.save()

            for item_receipt_form in formset:
                item_receipt = item_receipt_form.save(commit=False)
                item_receipt.item_info = itemreceiptinfo
                item_receipt.warehouse = itemreceiptinfo.warehouse
                item_receipt.save()

            messages.success(request, 'The post has been created successfully.')
            return redirect('itemreceipt_create')
        else:
            # Add form errors to messages framework
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')
                    
            for formset_error in formset.non_form_errors():
                messages.error(request, formset_error)
                
    else:
        form = ItemReceiptinfoForm()
        formset = ItemReceiptFormSet()

    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'item/itemreceipt/form.html', context)


def itemreceipt_update(request, pk):
    # Retrieve the success message from the query parameters
    success_message = request.GET.get('success_message')
    itemreceiptinfo = get_object_or_404(ItemReceiptinfo, pk=pk)
    ItemReceiptFormSet = inlineformset_factory(ItemReceiptinfo, ItemReceipt, form=ItemReceiptForm, fields=('item', 'quantity',),
                                               extra=1, can_delete=False, min_num=1, validate_min=True)

    if request.method == 'POST':
        form = ItemReceiptinfoForm(request.POST, instance=itemreceiptinfo)
        formset = ItemReceiptFormSet(request.POST, instance=itemreceiptinfo)

        if form.is_valid() and formset.is_valid():
            form.save()
            instances = formset.save(commit=False)  # Save the formset instances without committing to the database

            for instance in instances:
                instance.warehouse = itemreceiptinfo.warehouse  # Assign the warehouse value
                instance.save()

            formset.save()  # Save the many-to-many relationships, if any
            messages.success(request, 'The item has been updated successfully.')
            # Redirect to itemreceipt_update route
            return redirect('itemreceipt_create')
    else:
        form = ItemReceiptinfoForm(instance=itemreceiptinfo)
        formset = ItemReceiptFormSet(instance=itemreceiptinfo)

    context = {
        'form': form,
        'formset': formset,
        'itemreceiptinfo': itemreceiptinfo,
    }
    return render(request, 'item/itemreceipt/updateform.html', context)


def itemreceiptinfo_list(request):
    itemreceiptinfos = ItemReceiptinfo.objects.all()
    return render(request, 'item/itemreceipt/list.html', {'itemreceiptinfos': itemreceiptinfos})

def itemreceiptinfo_delete(request, pk):
    itemreceiptinfo = get_object_or_404(ItemReceiptinfo, pk=pk)
    
    if request.method == 'POST':
        itemreceiptinfo.delete()
        return redirect('itemreceiptinfo_list')
    
    return render(request, 'item/itemreceipt/delete.html', {'itemreceiptinfo': itemreceiptinfo})