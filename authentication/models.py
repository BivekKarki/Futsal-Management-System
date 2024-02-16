import uuid

from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class Consumer(models.Model):
    consumer_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=50) # emailfield(length=250)
    address = models.TextField(max_length=50) #textfield
    password = models.CharField(max_length=50)

    def __str__(self):
        return "%d   %s %s  %s  %s" % (self.consumer_id, self.name, self.phone, self.email, self.password)




