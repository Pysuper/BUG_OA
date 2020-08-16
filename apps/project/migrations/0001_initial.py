# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2020-08-16 08:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0002_auto_20200816_0837'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='项目名称')),
                ('color', models.SmallIntegerField(choices=[(1, '#56b8eb'), (2, '#f28033'), (3, '#ebc656'), (4, '#a2d148'), (5, '#20BFA4'), (6, '#7461c2'), (7, '#20bfa3')], default=1, verbose_name='颜色')),
                ('desc', models.CharField(blank=True, max_length=25, null=True, verbose_name='项目描述')),
                ('user_space', models.IntegerField(default=0, verbose_name='项目已使用空间')),
                ('star', models.BooleanField(default=0, verbose_name='星标')),
                ('bucket', models.CharField(max_length=128, verbose_name='腾讯对象存储桶')),
                ('region', models.CharField(max_length=32, verbose_name='腾讯对象存储区域')),
                ('join_count', models.SmallIntegerField(default=1, verbose_name='参与人数')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserInfo', verbose_name='创建者')),
            ],
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star', models.BooleanField(default=False, verbose_name='星标')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='加入时间')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.Project', verbose_name='项目名称')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.UserInfo', verbose_name='项目参与者')),
            ],
        ),
    ]
