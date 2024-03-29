from django.contrib import admin
from clients import models


@admin.register(models.Client)
class ClientAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)
