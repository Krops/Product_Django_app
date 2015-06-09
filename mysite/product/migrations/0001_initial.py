# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.BooleanField(verbose_name=False)),
                ('description', models.CharField(max_length=400)),
                ('price', models.FloatField()),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('modified_at', models.DateTimeField(verbose_name='date modified')),
            ],
        ),
    ]
