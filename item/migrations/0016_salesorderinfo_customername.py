# Generated by Django 4.2.2 on 2023-06-16 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0015_salesorderinfo_salesorderdelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='salesorderinfo',
            name='customername',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='item.businesspartner'),
        ),
    ]
