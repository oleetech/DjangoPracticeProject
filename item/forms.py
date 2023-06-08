from django import forms
from .models import Item
from .models import Warehouse

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name','location']  # Add any other fields you want to include

class ItemForm(forms.ModelForm):


    class Meta:
        model = Item
        fields = ['name', 'description','quantity','warehouse']