# Generated by Django 3.2.4 on 2023-02-06 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('super_dong', '0006_alter_myshit_invest_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='myshit',
            name='share',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=11, verbose_name='shares'),
        ),
    ]
