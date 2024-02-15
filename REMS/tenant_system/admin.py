from django.contrib import admin

# Register your models here.
from .models import TenantDetails

class TenantDetailsAdmin(admin.ModelAdmin):
    list_display = ('vchr_name',)


admin.site.register(TenantDetails,TenantDetailsAdmin)