from django.contrib import admin

# Register your models here.

from .models import Company


class CompanyAdmin(admin.ModelAdmin):
    list_display = ('cp_id', 'cp_name')


admin.site.register(Company, CompanyAdmin)

