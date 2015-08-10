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
            name='Dashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('dashboard_type', models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('summary', 'Summary')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'dashboards',
                'verbose_name': 'dashboard',
                'permissions': (('view_dashboard_private', 'Can see all private dashboard data'), ('view_dashboard_public', 'Can see all public dashboard data'), ('view_dashboard_summary', 'Can see all summary dashboard data')),
            },
        ),
        migrations.CreateModel(
            name='UserDashboard',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dashboards', models.ManyToManyField(to='controlinterface.Dashboard', related_name='dashboards')),
                ('default_dashboard', models.ForeignKey(related_name='default', to='controlinterface.Dashboard')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'user dashboard',
                'verbose_name_plural': 'users dashboards',
            },
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('type_of', models.CharField(choices=[('bars', 'Bar Graph'), ('last', 'Last'), ('lines', 'Lines'), ('pie', 'Pie Chart')], max_length=10)),
                ('data_from', models.CharField(max_length=20)),
                ('interval', models.CharField(max_length=20)),
                ('nulls', models.CharField(choices=[('omit', 'Omit')], blank=True, max_length=20, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'widget',
                'verbose_name_plural': 'widgets',
            },
        ),
        migrations.CreateModel(
            name='WidgetData',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('key', models.CharField(max_length=200)),
                ('source', models.CharField(choices=[('vumi', 'Vumi Go')], max_length=10)),
                ('data_type', models.CharField(choices=[('private', 'Private'), ('public', 'Public'), ('summary', 'Summary')], max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'widget data',
                'verbose_name_plural': 'widget data sources',
            },
        ),
        migrations.AddField(
            model_name='widget',
            name='data',
            field=models.ManyToManyField(to='controlinterface.WidgetData', blank=True),
        ),
        migrations.AddField(
            model_name='dashboard',
            name='widgets',
            field=models.ManyToManyField(to='controlinterface.Widget', blank=True),
        ),
    ]
