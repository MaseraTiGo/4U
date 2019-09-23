from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=16, default='123456')

class Token(models.Model):
    tuser = models.OneToOneField(to='User', on_delete=models.CASCADE)
    token = models.CharField(max_length=32)
