import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# Create your models here.
class FutsalOwner(models.Model):
    owner_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    email = models.EmailField(max_length=100)  # emailfield(length=250)
    address = models.TextField(max_length=100)  # textfield
    password = models.CharField(max_length=50)
    otp = models.CharField(max_length=25, default='0000')
    status = models.BooleanField(default=False)

    def __str__(self):
        return "%d   %s %s  %s  %s" % (self.id, self.name, self.phone, self.email, self.password)
