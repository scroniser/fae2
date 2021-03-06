# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-25 16:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscriptions', '0003_payment_subscriptionrate'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='payment',
            options={'ordering': ['reference_time', 'capture_time'], 'verbose_name': 'Payment', 'verbose_name_plural': 'Payments'},
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='token_date',
            new_name='capture_time',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='transaction_date',
            new_name='query_time',
        ),
        migrations.RenameField(
            model_name='payment',
            old_name='reference_date',
            new_name='reference_time',
        ),
        migrations.RemoveField(
            model_name='payment',
            name='name',
        ),
        migrations.AddField(
            model_name='payment',
            name='register_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
