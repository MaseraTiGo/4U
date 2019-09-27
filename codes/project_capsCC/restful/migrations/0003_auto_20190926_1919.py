# Generated by Django 2.2.5 on 2019-09-26 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restful', '0002_plugins'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.IntegerField(choices=[(0, 'admin'), (1, 'svip'), (2, 'vip'), (3, 'poor')], default=3),
        ),
        migrations.AlterField(
            model_name='plugins',
            name='download',
            field=models.IntegerField(default=466, verbose_name='statistics of downloads'),
        ),
        migrations.AlterField(
            model_name='plugins',
            name='my_download',
            field=models.IntegerField(default=126, verbose_name='statistics of my site downloads'),
        ),
    ]
