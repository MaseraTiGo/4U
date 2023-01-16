# Generated by Django 3.2.4 on 2023-01-10 14:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('super_dong', '0002_alter_myshit_status'),
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
    ]
