# Generated by Django 4.1.3 on 2022-11-09 15:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("DemijohnBackend", "0008_user_recurring_order_bottle_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="cart",
        ),
        migrations.RemoveField(
            model_name="user",
            name="previous_orders",
        ),
        migrations.AddField(
            model_name="cart",
            name="user_id",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name="previousorder",
            name="user_id",
            field=models.ForeignKey(
                default=-1,
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
