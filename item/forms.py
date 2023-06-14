from django import forms
from .models import Currency
from .models import Item
from .models import BusinessPartner
from .models import Warehouse
from .models import Unit


class ReusableForm(forms.Form):
    name = forms.CharField(required=True)

    class Meta:
        model = Item
        fields = ['name', 'description', 'quantity', 'warehouse', 'unit']

    def __init__(self, *args, **kwargs):
        super(ReusableForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'name':
                field.widget.attrs['disabled'] = True
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


    class Meta:
        model = Item
        fields = ['name', 'description','quantity','warehouse','unit']
    def __init__(self, *args, **kwargs):


        super(ItemForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'id': f"defaultForm-{field_name}",
            })          

class BusinessPartnerForm(forms.ModelForm):


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

