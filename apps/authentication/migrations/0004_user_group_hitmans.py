# Generated by Django 3.2.5 on 2021-07-14 06:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("authentication", "0003_user_state"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="group_hitmans",
            field=models.ManyToManyField(
                related_name="_authentication_user_group_hitmans_+",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
