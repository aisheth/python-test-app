from django.contrib import admin
from projects import models


@admin.register(models.Project)
class ProjectAdmin(admin.ModelAdmin):
    readonly_fields = ('created_by', )

    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(models.ProjectUser)

