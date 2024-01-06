import uuid

from django.contrib.auth.models import AbstractUser, User
from django.db import models


# Create your models here.
class Consumer(models.Model):
    consumer_id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    def __str__(self):
        return "%d   %s %s  %s  %s" % (self.consumer_id, self.name, self.phone, self.email, self.password)




