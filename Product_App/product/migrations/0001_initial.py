# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('title', models.CharField(max_length=60)),
                ('body', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=200)),
                ('slug', models.BooleanField(verbose_name='Slug')),
                ('description', models.TextField()),
                ('price', models.FloatField(default=0.0)),
                ('rate', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(verbose_name='date created')),
                ('modified_at', models.DateTimeField(verbose_name='date modified')),
            ],
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('rate', models.BooleanField(verbose_name='Liked')),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, default=1)),
                ('product', models.ForeignKey(to='product.Product', default=1)),
            ],
        ),
        migrations.AddField(
            model_name='post',
            name='product',
            field=models.ForeignKey(to='product.Product', default=1),
        ),
    ]
