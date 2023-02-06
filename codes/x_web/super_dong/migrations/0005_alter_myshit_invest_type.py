# Generated by Django 3.2.4 on 2023-01-31 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_dong', '0004_myshit_delta'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myshit',
            name='invest_type',
            field=models.SmallIntegerField(choices=[(0, 'saving'), (1, 'current_deposit'), (2, 'fixed_deposit'), (3, 'steady'), (4, 'monetary found'), (6, 'stocks')], default=0, verbose_name='invest type'),
        ),
    ]
