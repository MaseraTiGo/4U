# Generated by Django 3.2.4 on 2023-02-09 14:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('super_dong', '0001_myshit'), ('super_dong', '0002_alter_myshit_status'), ('super_dong', '0003_test'), ('super_dong', '0004_myshit_delta'), ('super_dong', '0005_alter_myshit_invest_type'), ('super_dong', '0006_alter_myshit_invest_type'), ('super_dong', '0007_myshit_share')]

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('name', models.CharField(default='123', max_length=32, verbose_name='dante')),
            ],
            options={
                'db_table': 'awesomeDong_my_test',
                'ordering': ('-create_time',),
            },
        ),
        migrations.CreateModel(
            name='MyShit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name='创建时间')),
                ('name', models.CharField(max_length=32, verbose_name='where the money is')),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='how many here is')),
                ('invest_type', models.SmallIntegerField(choices=[(0, 'saving'), (1, 'current_deposit'), (2, 'fixed_deposit'), (3, 'steady'), (4, 'monetary fund'), (5, 'bond fund'), (6, 'mixed fund'), (7, 'equity fund'), (8, 'stocks')], default=0, verbose_name='invest type')),
                ('net_worth', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='net_worth')),
                ('status', models.SmallIntegerField(choices=[(0, 'sell out'), (1, 'buy in'), (2, 'hold'), (3, 'on the way')], default=2, verbose_name='status')),
                ('app', models.SmallIntegerField(choices=[(0, 'alipay'), (1, 'wechat'), (2, 'invest bank')], default=2, verbose_name='money app')),
                ('ex_info', models.JSONField(default=dict, verbose_name='ex_info')),
                ('remark', models.CharField(max_length=128, verbose_name='remark')),
                ('delta', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='delta')),
                ('share', models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='shares')),
            ],
            options={
                'db_table': 'awesomeDong_my_shit',
                'ordering': ('-create_time',),
            },
        ),
    ]