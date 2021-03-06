# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-01 22:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('display_text', models.CharField(max_length=128)),
                ('href', models.URLField(verbose_name='Link URL')),
            ],
        ),
        migrations.CreateModel(
            name='Program',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('abbr', models.SlugField(max_length=3, verbose_name='Program ID')),
                ('air_days', models.TextField(choices=[('S', 'Sun'), ('M', 'Mon'), ('T', 'Tue'), ('W', 'Wed'), ('H', 'Thu'), ('F', 'Fri'), ('A', 'Sat'), ('D', 'Weekday'), ('E', 'Weekends'), ('X', 'Every Day'), (None, 'Day of Week')])),
            ],
        ),
        migrations.CreateModel(
            name='Showtime',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('duration', models.DurationField()),
                ('program', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.Program')),
            ],
        ),
        migrations.CreateModel(
            name='StaffProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=32)),
                ('last_name', models.CharField(max_length=32)),
                ('job_title', models.CharField(max_length=64)),
                ('picture', models.ImageField(upload_to='staff/')),
                ('email', models.EmailField(max_length=254, verbose_name='Contact Email')),
                ('phone', models.CharField(max_length=14, verbose_name='Phone Number')),
                ('bio', models.CharField(max_length=1048)),
                ('program', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='programs.Program')),
            ],
        ),
        migrations.AddField(
            model_name='link',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='programs.StaffProfile'),
        ),
    ]
