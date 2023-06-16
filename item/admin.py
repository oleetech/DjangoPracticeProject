from django.contrib import admin
from .models import Currency,Unit,Warehouse,Item,BusinessPartner ,ItemReceiptinfo,ItemReceipt,ItemDelivery,ItemDeliveryinfo,SalesOrderInfo,SalesOrderDelivery,Stock
# Register your models here.
admin.site.register(Currency)
admin.site.register(Unit)
admin.site.register(Warehouse)
admin.site.register(Item)
admin.site.register(Stock)
admin.site.register(ItemReceiptinfo)
admin.site.register(ItemReceipt)


admin.site.register(ItemDeliveryinfo)
admin.site.register(ItemDelivery)

admin.site.register(SalesOrderInfo)
admin.site.register(SalesOrderDelivery)
admin.site.register(BusinessPartner)