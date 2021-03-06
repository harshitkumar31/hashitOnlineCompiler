# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-09-02 14:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=1000)),
                ('difficulty', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submission_name', models.CharField(max_length=50)),
                ('program', models.CharField(max_length=2000)),
                ('output', models.CharField(max_length=1000)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Compiler.Problem')),
            ],
        ),
        migrations.CreateModel(
            name='Tests',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('test_name', models.CharField(max_length=20)),
                ('prog_input', models.CharField(max_length=1000)),
                ('output', models.CharField(max_length=1000)),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='tests',
            field=models.ManyToManyField(to='Compiler.Tests'),
        ),
    ]
