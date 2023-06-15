from django import forms
from django.core.exceptions import ValidationError

from .models import Currency
from .models import Item,ItemReceipt,ItemReceiptinfo
from .models import BusinessPartner
from .models import Warehouse
from .models import Unit
from django_select2.forms import Select2Widget
from django.forms.models import inlineformset_factory
class SearchForm(forms.Form):
    name = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.TextInput)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['description'].required = False

     
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })  


class CurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ['name','code']  # Add any other fields you want to include
    def __init__(self, *args, **kwargs):


        super(CurrencyForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['name']  # Add any other fields you want to include
    def __init__(self, *args, **kwargs):


        super(UnitForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })

class WarehouseForm(forms.ModelForm):
    class Meta:
        model = Warehouse
        fields = ['name','location']  # Add any other fields you want to include
    def __init__(self, *args, **kwargs):


        super(WarehouseForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })        


class ItemForm(forms.ModelForm):

    description = forms.CharField(widget=forms.TextInput)
    warehouse = forms.ModelChoiceField(
        queryset=Warehouse.objects.all(),
        widget=Select2Widget(attrs={'class': 'select2'})
    )

    class Meta:
        model = Item
        fields = ['name', 'description','warehouse','unit']
    def __init__(self, *args, **kwargs):


        super(ItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })          
            
class ItemReceiptinfoForm(forms.ModelForm):

    class Meta:
        model = ItemReceiptinfo
        fields = ['warehouse','docno','created']

    def __init__(self, *args, **kwargs):
        super(ItemReceiptinfoForm, self).__init__(*args, **kwargs)
        last_docno = ItemReceiptinfo.objects.last().docno if ItemReceiptinfo.objects.exists() else 0
        self.fields['docno'].initial = last_docno + 1
        self.fields['docno'].widget.attrs['disabled'] = True
        self.fields['docno'].required = False
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })  
            
             
class ItemReceiptForm(forms.ModelForm):

    class Meta:
        model = ItemReceipt
        fields = ('item', 'quantity')
        
    def __init__(self, *args, **kwargs):
    

        super(ItemReceiptForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control input-xs',
                'id': f"defaultForm-{field_name}",
            })  





        
        
class BusinessPartnerForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput)

    class Meta:
        model = BusinessPartner
        fields = ['code','name', 'address','currency','currency_type','vendor_type']     

    def __init__(self, *args, **kwargs):


        super(BusinessPartnerForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })             

