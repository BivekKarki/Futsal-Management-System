from django.contrib import admin

from futsalOwner.models import FutsalOwner


class FutsalOwnerAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'name', 'phone', 'email')
    search_fields = ('name', 'phone', 'email')


# Register your models here.
admin.site.register(FutsalOwner, FutsalOwnerAdmin)
