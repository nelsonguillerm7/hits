# Generated by Django 3.2.5 on 2021-07-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="user",
            options={"verbose_name": "User", "verbose_name_plural": "Users"},
        ),
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(
                error_messages={"unique": "A user with this email already exists"},
                max_length=254,
                unique=True,
            ),
        ),
    ]
