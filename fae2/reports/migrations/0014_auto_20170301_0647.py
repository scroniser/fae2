# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-01 12:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0013_auto_20170228_1715'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='excludedurl',
            options={'ordering': ['file_type', 'url'], 'verbose_name': 'URL: Excluded URL', 'verbose_name_plural': 'URL: Excluded URL'},
        ),
        migrations.AlterModelOptions(
            name='excludedurlpagereference',
            options={'ordering': ['url'], 'verbose_name': 'URL: Page Reference for Excluded URLs', 'verbose_name_plural': 'URL: Page Reference for Excluded URLs'},
        ),
        migrations.RemoveField(
            model_name='excludedurl',
            name='reference_count',
        ),
    ]
