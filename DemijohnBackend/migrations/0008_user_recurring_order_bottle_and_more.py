# Generated by Django 4.1.3 on 2022-11-08 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DemijohnBackend", "0007_user_address_alter_user_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="recurring_order_bottle",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="user",
            name="recurring_order_type",
            field=models.CharField(default="", max_length=50),
        ),
    ]
