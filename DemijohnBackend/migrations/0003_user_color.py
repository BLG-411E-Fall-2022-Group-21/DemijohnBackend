# Generated by Django 4.1.3 on 2022-11-08 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("DemijohnBackend", "0002_alter_user_options_alter_user_managers_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="color",
            field=models.CharField(default="white", max_length=50),
        ),
    ]