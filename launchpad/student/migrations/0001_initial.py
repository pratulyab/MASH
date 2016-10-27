# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-10-27 18:59
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('college', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=60, unique=True, verbose_name='Name')),
                ('desc', models.TextField(blank=True, verbose_name='Description')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=40, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=40, verbose_name='Last Name')),
                ('gender', models.CharField(blank=True, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], default='M', max_length=1, verbose_name='Gender')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date Of Birth')),
                ('email', models.EmailField(error_messages={'unique': 'Student with email address already exists.'}, max_length=254, unique=True, verbose_name='Email ID')),
                ('phone_number', models.CharField(error_messages={'unique': 'Student with that phone number already exists.'}, help_text='10 Digit IN Number', max_length=10, unique=True, validators=[django.core.validators.RegexValidator(message="_('Invalid IN phone number. Make sure not to \t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\tprefix the number with either +91 or 0.')", regex='^[7-9]\\d{9}$')], verbose_name='Phone Number')),
                ('year', models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')], max_length=1, verbose_name='Current Year')),
                ('resume', models.URLField(help_text="Dropbox link to the student's recently uploaded resume.", validators=[django.core.validators.RegexValidator(flags=2, message='Invalid dropbox folder link', regex='^https?://(www\\.)?dropbox.*$')], verbose_name='Dropbox Link')),
                ('work_from_home', models.BooleanField(default=False, help_text='Prefer work from home?')),
                ('credits', models.DecimalField(decimal_places=2, default=0, max_digits=5, validators=[django.core.validators.MinValueValidator(Decimal('0'))])),
                ('availibility', models.BooleanField(default=True)),
                ('experiences', models.TextField(blank=True, help_text='Details about the experiences in the mentioned domains (if any)', verbose_name='Domain Experiences')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('college', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='college.College')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='students', to='college.Course')),
                ('interested_domains', models.ManyToManyField(help_text='Domains interested in for internship', related_name='students', to='student.Domain', verbose_name='Interests')),
            ],
        ),
    ]
