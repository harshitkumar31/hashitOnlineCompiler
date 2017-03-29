# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-02 18:26
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Compiler', '0003_remove_solution_output'),
    ]

    operations = [
        migrations.AddField(
            model_name='solution',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
