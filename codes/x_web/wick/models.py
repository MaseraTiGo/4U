from django.db import models


# Create your models here.

class Migrations(models.Model):
    name = models.CharField(verbose_name='migration name', max_length=128,
                            null=False)
    content = models.TextField(verbose_name='content', null=False)
    app = models.CharField(verbose_name='app name', max_length=32, null=False)
    path = models.CharField(verbose_name='migration file path', max_length=255,
                            null=False)
    index = models.SmallIntegerField(verbose_name='index', default=0)
    ex_info = models.JSONField(verbose_name='ex info', default=dict)
