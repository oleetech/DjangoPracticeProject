from django.contrib import admin
from .models import Currency,Unit,Warehouse,Item,BusinessPartner 
# Register your models here.
admin.site.register(Currency)
admin.site.register(Unit)
admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(BusinessPartner)