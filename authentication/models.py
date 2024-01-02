from django.db import models

# Create your models here.
class Consumer(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length=50)

    def __str__(self):
        return "%s   %s" % (self.consumer_id, self.name)
