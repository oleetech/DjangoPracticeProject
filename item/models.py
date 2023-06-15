from os import name
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Currency(models.Model):
    name = models.CharField(max_length=100,unique=True)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
    
class Unit(models.Model):
    name=models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class Warehouse(models.Model):
    name = models.CharField(max_length=100,unique=True)
    location = models.CharField(max_length=100)
    # Add any other fields for the Warehouse model

    def __str__(self):
        return self.name

class Item(models.Model):
    name = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    quantity = models.PositiveIntegerField()
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE,default=1)
    unit = models.ForeignKey(Unit, on_delete=models.SET_DEFAULT, default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Add any other fields you need

    def __str__(self):
        return self.name

class ItemReceiptinfo(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    docno = models.PositiveIntegerField(default=1,unique=True)
    created = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f" {self.docno}"
        
class ItemReceipt(models.Model):
    item_info = models.ForeignKey(ItemReceiptinfo, on_delete=models.CASCADE, null=True, default=None)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f" {self.item_info.docno}"

    def clean(self):
        if self.quantity == 0:
            raise ValidationError("Quantity cannot be 0.")
  
class ItemDelivery(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f"ItemDelivery: {self.item.name} - {self.quantity}"
class Stock(models.Model):
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

class BusinessPartner(models.Model):
    code = models.CharField(max_length=50,unique=True)
    name = models.CharField(max_length=100,unique=True)
    address = models.TextField()
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT,default=1)

    CURRENCY_TYPES = [
        ('local', 'Local Currency'),
        ('foreign', 'Foreign Currency'),
    ]
    currency_type = models.CharField(max_length=10, choices=CURRENCY_TYPES,default='local')

    VENDOR_TYPES = [
        ('supplier', 'Supplier'),
        ('customer', 'Customer'),
    ]
    vendor_type = models.CharField(max_length=10, choices=VENDOR_TYPES,default='customer')

    def __str__(self):
        return self.name   