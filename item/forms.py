from django import forms
from .models import Item
from .models import BusinessPartner
from .models import Warehouse
from .models import Unit

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']  # Add any other fields you want to include

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name','location']  # Add any other fields you want to include

class ItemForm(forms.ModelForm):


    class Meta:
        model = Item
        fields = ['name', 'description','quantity','warehouse','unit']

class BusinessPartnerForm(forms.ModelForm):


    class Meta:
        model = BusinessPartner
        fields = ['code','name', 'address','currency','currency_type','vendor_type']        