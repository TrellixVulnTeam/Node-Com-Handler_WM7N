# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-23 20:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.CharField(max_length=200)),
                ('first_connect', models.DateTimeField(verbose_name='date first accessed on address')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_version', models.CharField(max_length=1)),
                ('country', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('region', models.CharField(max_length=100)),
                ('postal_code', models.IntegerField(max_length=6)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plex.Address')),
            ],
        ),
    ]