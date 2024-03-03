from django.contrib import admin
from authentication.models import Consumer, UserRole


class ConsumerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone', 'email')


# Register your models here.
admin.site.register(Consumer, ConsumerAdmin)
admin.site.register(UserRole)
