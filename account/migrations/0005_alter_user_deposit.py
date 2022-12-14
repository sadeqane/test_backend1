# Generated by Django 4.1 on 2022-08-19 15:01

import backend1.helpers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_options_remove_user_date_joined_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='deposit',
            field=models.PositiveIntegerField(default=0, validators=[backend1.helpers.deposit_should_be_multiply_5]),
        ),
    ]
