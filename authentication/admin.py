from django.contrib import admin
from authentication.models import Consumer


class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('consumer_id', 'name', 'phone', 'email')


# Register your models here.
admin.site.register(Consumer, ConsumerAdmin)
