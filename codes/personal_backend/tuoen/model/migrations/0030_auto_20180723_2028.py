# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2018-07-23 20:28
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('model', '0029_departmentchange'),
    ]

    operations = [
        migrations.CreateModel(
            name='Replenishment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('replenishment_num', models.CharField(default='', max_length=64, verbose_name='补货單號')),
                ('quantity', models.IntegerField(default=0, verbose_name='数量')),
                ('remark', models.CharField(default='', max_length=128, verbose_name='備註')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.Customer')),
                ('order', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.Order')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReplenishmentEvent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.TextField(default='', null=True, verbose_name='备注')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('describe', models.TextField(default='', null=True, verbose_name='描述')),
                ('department', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.Department')),
                ('replenishment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Replenishment')),
                ('staff', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='model.Staff')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReplenishmentItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('remark', models.CharField(default='', max_length=128, verbose_name='備註')),
                ('status', models.CharField(default='', max_length=64, verbose_name='补货状态')),
                ('amount', models.IntegerField(default=0, verbose_name='金额')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='equipment',
            name='equipment_status',
            field=models.CharField(choices=[('normal', '正常'), ('replace', '售后机'), ('patch', '补货'), ('rgoods', '注册并退货'), ('abnormal', '异常')], default='normal', max_length=64, verbose_name='设备状态'),
        ),
        migrations.AddField(
            model_name='replenishmentitem',
            name='code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Equipment'),
        ),
        migrations.AddField(
            model_name='replenishmentitem',
            name='goods',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Goods'),
        ),
        migrations.AddField(
            model_name='replenishmentitem',
            name='replenishment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='model.Replenishment'),
        ),
    ]
