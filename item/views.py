from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse


from django.core.exceptions import ValidationError
from django.forms import formset_factory, inlineformset_factory
from .models import ItemReceipt, ItemReceiptinfo,ItemDeliveryinfo,ItemDelivery,SalesOrderInfo,SalesOrderDelivery,Stock
from .forms import ItemReceiptinfoForm,ItemReceiptForm,ItemDeliveryinfoForm,ItemDeliveryForm,SalesOrderInfoForm,SalesOrderDeliveryForm,StockForm


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

def stock_create(request):
    success_message = request.GET.get('success_message')

    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'The stock has been created successfully.')
            return redirect('stock_create')
    else:
        form = StockForm()
        context = {'form': form,'page_title': 'Create Stock'}

    return render(request, 'item/create.html',context )



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
        extra=0,
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

            for formset_form in formset.forms:
                item_receipt = formset_form.save(commit=False)
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
        'formset': formset,
        'page_title': 'Create Item Receipt'  # Set the page title here
    }
    return render(request, 'item/itemreceipt/form.html', context)




def itemreceipt_update(request, pk):
    # Retrieve the success message from the query parameters
    success_message = request.GET.get('success_message')
    itemreceiptinfo = get_object_or_404(ItemReceiptinfo, pk=pk)
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
        form = ItemReceiptinfoForm(request.POST, instance=itemreceiptinfo)
        formset = ItemReceiptFormSet(request.POST, instance=itemreceiptinfo)

        if form.is_valid() and formset.is_valid():
            form.save()
            
            for formset_form in formset.forms:
                if formset_form.has_changed():
                    item_receipt = formset_form.save(commit=False)
                    item_receipt.item_info = itemreceiptinfo
                    item_receipt.warehouse = itemreceiptinfo.warehouse
                    item_receipt.save()
            
            messages.success(request, 'The post has been updated successfully.')
            return redirect('itemreceipt_create')
        else:
            # Add form errors to messages framework
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')
                    
            for formset_error in formset.non_form_errors():
                messages.error(request, formset_error)
                
    else:
        form = ItemReceiptinfoForm(instance=itemreceiptinfo)
        formset = ItemReceiptFormSet(instance=itemreceiptinfo)

    context = {
        'form': form,
        'formset': formset
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




def itemdelivery_create(request):
    ItemDeliveryFormSet = inlineformset_factory(
        ItemDeliveryinfo,
        ItemDelivery,
        form=ItemDeliveryForm,
        fields=('item', 'quantity'),
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True
    )

    if request.method == 'POST':
        form = ItemDeliveryinfoForm(request.POST)
        formset = ItemDeliveryFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            last_item_deliveryinfo = ItemDeliveryinfo.objects.last()

            if last_item_deliveryinfo:
                new_docno = last_item_deliveryinfo.docno + 1
            else:
                new_docno = 1

            itemdeliveryinfo = form.save(commit=False)
            itemdeliveryinfo.docno = new_docno
            itemdeliveryinfo.save()

            for item_delivery_form in formset:
                item_delivery = item_delivery_form.save(commit=False)
                item_delivery.item_info = itemdeliveryinfo
                item_delivery.warehouse = itemdeliveryinfo.warehouse
                item_delivery.save()

            messages.success(request, 'The post has been created successfully.')
            return redirect('itemdelivery_create')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')

            for formset_error in formset.non_form_errors():
                messages.error(request, formset_error)

    else:
        form = ItemDeliveryinfoForm()
        formset = ItemDeliveryFormSet()

    context = {
        'form': form,
        'formset': formset,
        'page_title': 'Create Item Delivery'  # Set the page title here

    }
    return render(request, 'item/itemreceipt/form.html', context)


def itemdelivey_update(request, pk):
    # Retrieve the success message from the query parameters
    success_message = request.GET.get('success_message')
    itemdeliveryinfo = get_object_or_404(ItemDeliveryinfo, pk=pk)
    ItemDeliveryFormSet = inlineformset_factory(
        ItemDeliveryinfo,
        ItemDelivery,
        form=ItemDeliveryForm,
        fields=('item', 'quantity'),
        extra=1,
        can_delete=False,
        min_num=1,
        validate_min=True
    )

    if request.method == 'POST':
        form = ItemDeliveryinfoForm(request.POST, instance=itemdeliveryinfo)
        formset = ItemDeliveryFormSet(request.POST, instance=itemdeliveryinfo)

        if form.is_valid() and formset.is_valid():
            form.save()

            for formset_form in formset.forms:
                if formset_form.has_changed():
                    item_delivery = formset_form.save(commit=False)
                    item_delivery.item_info = itemdeliveryinfo
                    item_delivery.warehouse = itemdeliveryinfo.warehouse
                    item_delivery.save()

            messages.success(request, 'The post has been updated successfully.')
            return redirect('itemdelivery_create')
        else:
            # Add form errors to messages framework
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')

            for formset_error in formset.non_form_errors():
                messages.error(request, formset_error)

    else:
        form = ItemDeliveryinfoForm(instance=itemdeliveryinfo)
        formset = ItemDeliveryFormSet(instance=itemdeliveryinfo)

    context = {
        'form': form,
        'formset': formset
    }
    return render(request, 'item/itemreceipt/updateform.html', context)

def itemdeliveryinfo_list(request):
    itemdeliveryinfos = ItemDeliveryinfo.objects.all()
    context = {'itemreceiptinfos': itemdeliveryinfos, 'page_title': ' Item Delivery list' }
    return render(request, 'item/itemreceipt/itemdeliverylist.html',context )

def itemdeliveryinfo_delete(request, pk):
    itemdeliveryinfo = get_object_or_404(ItemDeliveryinfo, pk=pk)
    
    if request.method == 'POST':
        itemdeliveryinfo.delete()
        return redirect('itemdeliveryinfo_list')
    
    return render(request, 'item/itemreceipt/delete-goods-delivery.html', {'itemdeliveryinfo': itemdeliveryinfo})


def salesorder_create(request):
    SalesOrderDeliveryFormSet = inlineformset_factory(
        SalesOrderInfo,
        SalesOrderDelivery,
        form=SalesOrderDeliveryForm,
        fields=('item', 'quantity', 'price'),
        extra=0,  # Initial extra value set to 0
        can_delete=False,
        min_num=1,
        validate_min=True
    )

    if request.method == 'POST':
        form = SalesOrderInfoForm(request.POST)
        formset = SalesOrderDeliveryFormSet(request.POST)

        extra_value = int(request.POST.get('extra_value', 0))  # Retrieve the extra_value from the form submission

        # Update the extra value of the formset based on extra_value
        SalesOrderDeliveryFormSet.extra = extra_value

        if form.is_valid() and formset.is_valid():
            # Calculate auto document no
            last_item_salesinfo = SalesOrderInfo.objects.last()

            if last_item_salesinfo:
                new_docno = last_item_salesinfo.order_number + 1
            else:
                new_docno = 1
            sales_order_info = form.save(commit=False)
            sales_order_info.order_number = new_docno

            # Calculate and set the total_amount
            total_amount = sum(
                form.cleaned_data['quantity'] * form.cleaned_data['price']
                for form in formset.forms
            )
            sales_order_info.total_amount = total_amount

            # Save the sales_order_info instance to assign a primary key
            sales_order_info.save()

            for form in formset.forms:
                if form.has_changed() and form.cleaned_data.get('quantity', 0) > 0:
                    sales_order_delivery = form.save(commit=False)
                    sales_order_delivery.order_info = sales_order_info
                    sales_order_delivery.price_total = (
                        sales_order_delivery.quantity * sales_order_delivery.price
                    )
                    sales_order_delivery.save()

            messages.success(request, 'The sales order has been created successfully.')
            return redirect('salesorder_create')
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')

            for formset_error in formset.non_form_errors():
                messages.error(request, formset_error)

    else:
        form = SalesOrderInfoForm()
        formset = SalesOrderDeliveryFormSet()

    context = {
        'form': form,
        'formset': formset,
        'page_title': 'Create Sales Order'
    }
    return render(request, 'item/itemreceipt/form.html', context)




def salesorder_update(request, pk):
    sales_order_info = get_object_or_404(SalesOrderInfo, pk=pk)
    SalesOrderDeliveryFormSet = inlineformset_factory(
        SalesOrderInfo,
        SalesOrderDelivery,
        form=SalesOrderDeliveryForm,
        fields=('item', 'quantity', 'price'),
        extra=0,
        can_delete=False,
        min_num=1,
        validate_min=True
    )

    if request.method == 'POST':
        form = SalesOrderInfoForm(request.POST, instance=sales_order_info)
        formset = SalesOrderDeliveryFormSet(request.POST, instance=sales_order_info)

        if form.is_valid() and formset.is_valid():
            sales_order_info = form.save(commit=False)

            # Calculate and set the total_amount
            total_amount = sum(
                formset.cleaned_data['quantity'] * formset.cleaned_data['price']
                for formset in formset.forms
            )
            sales_order_info.total_amount = total_amount

            sales_order_info.save()

            for formset_form in formset.forms:
                if formset_form.has_changed():
                    sales_order_delivery = formset_form.save(commit=False)
                    sales_order_delivery.order_info = sales_order_info
                    sales_order_delivery.price_total = (
                        sales_order_delivery.quantity * sales_order_delivery.price
                    )
                    sales_order_delivery.save()

            messages.success(request, 'The sales order has been updated successfully.')
            return redirect('salesorder_update', pk=pk)
        else:
            for field, error_list in form.errors.items():
                for error in error_list:
                    messages.error(request, f'{field}: {error}')

            for formset_error in formset.non_form_errors():
                messages.error(request, formset_error)

    else:
        form = SalesOrderInfoForm(instance=sales_order_info)
        formset = SalesOrderDeliveryFormSet(instance=sales_order_info)

    context = {
        'form': form,
        'formset': formset,
        'page_title': 'Update Sales Order'
    }
    return render(request, 'item/itemreceipt/updateform.html', context)


def salesorder_info_list(request):
    salesorderinfos = SalesOrderInfo.objects.all()
    context = {'salesorderinfos': salesorderinfos, 'page_title': 'Sales Order List'}
    return render(request, 'item/salesorder/list.html', context)

def salesorder_info_delete(request, pk):
    salesorderinfo = get_object_or_404(SalesOrderInfo, pk=pk)

    if request.method == 'POST':
        salesorderinfo.delete()
        return redirect('salesorder_info_list')

    return render(request, 'item/salesorder/delete.html', {'salesorderinfo': salesorderinfo})
