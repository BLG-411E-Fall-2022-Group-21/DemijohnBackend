# Generated by Django 4.1.3 on 2022-12-10 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DemijohnBackend", "0010_alter_user_address_alter_user_password_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cart",
            name="water_type",
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name="previousorder",
            name="water_type",
            field=models.CharField(max_length=250),
        ),
    ]
