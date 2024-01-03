from django.contrib import admin

from authentication.models import Consumer, Profile

# Register your models here.
admin.site.register(Consumer)
admin.site.register(Profile)